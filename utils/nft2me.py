from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
from settings import QUANTITY_NFT_15
import random
from utils.retry import exception_handler

contracts = ['0x79E816b618B236E94cd08E25495015d4b0cADA42', '0x56526Ad6a315b3A7D68d65750fc7eB7c9fD47c2E',
             '0x49a015d2AC7D2E258E56f8867c17c783A1E54248', '0x2a95cc258010c723adcc619d2d63fD1d16253269',
             '0xE240272CBdc287D880164c45E96F4a2461397Db5', '0x320237de8bEc260E2FDf16349DC9617e4711F9F2']


class NFT2ME(Wallet):

    def __init__(self, private_key, chain_from, number, proxy):
        super().__init__(private_key, chain_from, number, proxy)
        self.abi = js.load(open('./abi/nft2me.txt'))
        self.contract = self.web3.eth.contract(address=Web3.to_checksum_address(random.choice(contracts)), abi=self.abi)

    @exception_handler
    def mint(self):
        quantity = random.randint(QUANTITY_NFT_15[0], QUANTITY_NFT_15[1])
        name = self.contract.functions.name().call
        logger.info(f'Mint {quantity} {name} on NFT2ME || Zora chain')
        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        contract_txn = self.contract.functions.mint(quantity).build_transaction(dick)
        self.send_transaction_and_wait(contract_txn, f'Mint {quantity} {name} on NFT2ME')
