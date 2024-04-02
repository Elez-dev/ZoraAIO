from utils.retry_refuel import exception_handler_refuel
from utils.wallet import Wallet
from settings import CHAIN_FROM_REFUEL, VALUE_REFUEL
from web3 import Web3
from loguru import logger
import random
from utils.func import crypto_prices

chain_id = {
    'Zora': 7777777,
    'Arbitrum': 42161,
    'Optimism': 10,
    'Nova': 42170,
    'Base': 8453,
    'zkSync': 324,
    'Linea': 59144
}


class Refuel(Wallet):
    def __init__(self, private_key, chain_to, number, proxy):
        self.private_key = private_key
        super().__init__(private_key, self.get_refuel_chain(), number, proxy)
        self.chain_to = chain_to

    @exception_handler_refuel
    def get_refuel_chain(self):

        balance_chain = 0
        chan = None

        for chain in CHAIN_FROM_REFUEL:
            web3 = self.get_web3_refuel(chain)
            address_wallet = web3.eth.account.from_key(self.private_key).address
            balance = web3.eth.get_balance(address_wallet)
            if chain == 'Polygon':
                value = float(Web3.from_wei(balance, "ether")) * crypto_prices['wmatic']
            else:
                value = float(Web3.from_wei(balance, "ether")) * crypto_prices['ethereum']

            logger.info(f'Баланс в {chain} - {Web3.from_wei(balance, "ether")}')

            if balance_chain > value:
                continue
            else:
                balance_chain = value
                chan = chain

        logger.success(f'Cеть для рефуела - {chan}\n')
        return chan

    @exception_handler_refuel
    def refuel(self):
        if self.chain == self.chain_to:
            return 'error'

        logger.info(f'Relay bridge || {self.chain} -> {self.chain_to}')

        if self.chain == 'Polygon':
            value = VALUE_REFUEL['Polygon']
            token = 'Matic'
        else:
            value = VALUE_REFUEL['Other']
            token = 'ETH'
        value = Web3.to_wei(round(random.uniform(value[0], value[1]), value[2]), 'ether')
        balance = self.get_native_balance()

        json = {
            'originChainId': chain_id[self.chain],
            'destinationChainId': chain_id[self.chain_to],
            'user': self.address_wallet,
            'txs': [{
                'data': '0x',
                'to': self.address_wallet,
                'value': str(value)
            }]
        }

        data = self.get_api_call_data_post('https://api.relay.link/execute/call', json)

        value = int(data['steps'][0]['items'][0]['data']['value'])

        if balance < value:
            value = (balance * 0.7)

        if value <= 0:
            logger.error(f'Value bridge {token} - {value}\n')
            return

        dick = {
            'chainId': self.web3.eth.chain_id,
            'from': self.address_wallet,
            'data': data['steps'][0]['items'][0]['data']['data'],
            'to': Web3.to_checksum_address(data['steps'][0]['items'][0]['data']['to']),
            'value': value,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        gas = int(self.web3.eth.estimate_gas(dick) * 1.3)
        dick.update({'gas': gas})

        self.send_transaction_and_wait(dick, f'Relay bridge {round(Web3.from_wei(value, "ether"), 5)} {token} || {self.chain} -> {self.chain_to}')
