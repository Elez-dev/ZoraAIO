import random
from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
import json as js
from settings import OFF_ZORA_DEPOSIT
from utils.retry import exception_handler


class ZoraBridge(Wallet):

    def __init__(self, private_key, number):
        super().__init__(private_key, 'Ethereum', number, None)
        self.address = Web3.to_checksum_address('0x1a0ad011913A150f69f6A19DF447A0CfD9551054')
        self.abi = js.load(open('./abi/of_bridge.txt'))
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    @exception_handler
    def bridge(self):
        value = Web3.to_wei(round(random.uniform(OFF_ZORA_DEPOSIT[0], OFF_ZORA_DEPOSIT[1]), OFF_ZORA_DEPOSIT[2]), 'ether')
        gas = 60_000
        balance = self.get_native_balance()
        gas_cost = self.web3.eth.gas_price * gas
        if balance - gas_cost < 0:
            logger.error('Balance ETH - GasCost < 0\n')
            return

        if balance - gas_cost < value:
            value = balance - gas_cost

        if value <= 0:
            logger.error(f'Value bridge ETH - {value}\n')
            return

        dick = {
            'from': self.address_wallet,
            'value': value,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': gas,
            **self.get_gas_price()
        }
        txn = self.contract.functions.depositTransaction(self.address_wallet, value, 100000, False, b'').build_transaction(dick)
        self.send_transaction_and_wait(txn, f'Zora bridge {Web3.from_wei(value, "ether")} ETH || ETH -> Zora')
