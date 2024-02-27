from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
import random
from settings import PRESCALE
from utils.retry import exception_handler


class WrapETH(Wallet):
    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.address = Web3.to_checksum_address('0x4200000000000000000000000000000000000006')
        self.abi = js.load(open('./abi/wrap.txt'))
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    @exception_handler
    def wrap(self):
        logger.info('Wrap ETH')
        balance = self.web3.eth.get_balance(self.address_wallet)
        if balance < Web3.to_wei(0.00001, 'ether'):
            logger.info('Insufficient funds')
            return 'balance'
        prescale = round(random.uniform(PRESCALE[0], PRESCALE[1]), PRESCALE[2])
        value = int(balance * prescale)

        dick = {
            "from": self.address_wallet,
            "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            "value": value,
            **self.get_gas_price()

        }

        contract_txn = self.contract.functions.deposit().build_transaction(dick)

        self.send_transaction_and_wait(contract_txn, f'Wrap {round(Web3.from_wei(value, "ether"), 6)} ETH')

    @exception_handler
    def unwrap(self):
        logger.info('Unwrap ETH')
        token_balance = self.contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            return logger.error('Balance WETH - 0\n')

        dick = {
            "from": self.address_wallet,
            "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()

        }

        contract_txn = self.contract.functions.withdraw(token_balance).build_transaction(dick)

        self.send_transaction_and_wait(contract_txn, f'Unwrap {round(Web3.from_wei(token_balance, "ether"), 6)} ETH')
