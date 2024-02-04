import random
from web3 import Web3
import time
from settings import CHAIN_RPC
from web3.middleware import geth_poa_middleware
from requests.adapters import Retry
from utils.retry_wallet import exception_handler_wallet
import requests
from loguru import logger
from settings import ZORA_GASPRICE_PRESCALE, BASE_GASPRICE_PRESCALE, TG_BOT_SEND
from utils.tg_bot import TgBot

SCAN = {
    'Ethereum': 'https://etherscan.io/tx/',
    'Arbitrum': 'https://arbiscan.io/tx/',
    'Optimism': 'https://optimistic.etherscan.io/tx/',
    'Polygon': 'https://polygonscan.com/tx/',
    'Base': 'https://basescan.org/tx/',
    'Zora': 'https://explorer.zora.energy/tx/',
    'Nova': 'https://nova.arbiscan.io/tx/',
    'zkSync': 'https://era.zksync.network/tx/',
    'Linea': 'https://lineascan.build/tx/'
}


class Wallet(TgBot):

    def __init__(self, private_key, chain, number, proxy):
        self.private_key = private_key
        self.chain = chain
        self.number = number
        self.proxy = proxy
        self.web3 = self.get_web3(chain)
        self.scan = self.get_scan(chain)
        self.account = self.web3.eth.account.from_key(private_key)
        self.address_wallet = self.account.address

    def get_web3(self, chain):
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        if self.proxy is not None:
            proxy_dick = {'https': 'http://' + self.proxy, 'http': 'http://' + self.proxy}
            session.proxies = proxy_dick
        return Web3(Web3.HTTPProvider(CHAIN_RPC[chain], request_kwargs={'timeout': 60}, session=session))

    @staticmethod
    def get_scan(chain):
        return SCAN[chain]

    @staticmethod
    def to_wei(decimal, amount):
        if decimal == 6:
            unit = 'picoether'
        else:
            unit = 'ether'

        return Web3.to_wei(amount, unit)

    @staticmethod
    def from_wei(decimal, amount):
        if decimal == 6:
            unit = 'picoether'
        elif decimal == 8:
            return float(amount / 10 ** 8)
        else:
            unit = 'ether'

        return Web3.from_wei(amount, unit)

    def send_transaction_and_wait(self, tx, message):
        signed_txn = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info('Sent a transaction')
        time.sleep(5)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=900, poll_latency=5)
        if tx_receipt.status == 1:
            logger.success('The transaction was successfully mined')
        else:
            logger.error("Transaction failed, I'm trying again")
            if TG_BOT_SEND is True:
                TgBot.send_message_error(self, self.number, message, self.address_wallet, "Transaction failed, I'm trying again")
            raise ValueError('')

        if TG_BOT_SEND is True:
            TgBot.send_message_success(self, self.number, message, self.address_wallet, f'{self.scan}{tx_hash.hex()}')

        logger.success(f'[{self.number}] {message} || {self.scan}{tx_hash.hex()}\n')
        return tx_hash

    def get_native_balance(self):
        return self.web3.eth.get_balance(self.address_wallet)

    def get_gas_price(self):
        if self.chain in ["Polygon", "Avax", 'Zora']:
            try:
                self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            except:
                pass

        if self.chain == 'Zora':
            return {'maxFeePerGas': Web3.to_wei(ZORA_GASPRICE_PRESCALE, 'gwei'), 'maxPriorityFeePerGas': Web3.to_wei(ZORA_GASPRICE_PRESCALE, 'gwei')}
        elif self.chain == 'Base':
            return {'maxFeePerGas': int(self.web3.eth.gas_price * BASE_GASPRICE_PRESCALE), 'maxPriorityFeePerGas': int(self.web3.eth.max_priority_fee * BASE_GASPRICE_PRESCALE)}
        return {'maxFeePerGas': self.web3.eth.gas_price, 'maxPriorityFeePerGas': self.web3.eth.max_priority_fee}

    @staticmethod
    def get_api_call_data_post(url, json):

        with requests.Session() as s:
            call_data = s.post(url, json=json, timeout=60)
        if call_data.status_code < 400:
            api_data = call_data.json()
            return api_data
        else:
            logger.error("Couldn't get a response")
            raise ValueError('')

    @exception_handler_wallet
    def transfer_native(self, address, value=None):

        balance = self.get_native_balance()
        if balance - Web3.to_wei(0.00005, 'ether') <= 0:
            logger.error(f'Balance ETH < 0.00005\n')
            return

        if value is None:
            max_value = balance - Web3.to_wei(0.00005, 'ether')
            min_value = int(balance / 100)
            value = round(Web3.from_wei(random.randint(min_value, max_value), 'ether'), 6)

        amount = Web3.to_wei(value, 'ether')

        dick = {
            'chainId': self.web3.eth.chain_id,
            'from': self.address_wallet,
            'to': Web3.to_checksum_address(address),
            'value': amount,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 21_000,
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(dick, f'Transfer {Web3.from_wei(amount, "ether")} ETH to {address}')
