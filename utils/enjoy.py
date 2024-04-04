from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
from utils.func import sleeping
from settings import QUANTITY_NFT_31, QUANTITY_NFT_32
import json as js
import random


class MintForEnjoy(Wallet):
    def __init__(self, private_key, number, proxy):
        super().__init__(private_key, 'Zora', number, proxy)
        self.address = Web3.to_checksum_address('0x777777E8850d8D6d98De2B5f64fae401F96eFF31')
        self.abi = js.load(open('./abi/erc20minter.txt'))
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        self.enjoy = Web3.to_checksum_address('0xa6B280B42CB0b7c4a4F789eC6cCC3a7609A1Bc39')
        self.imagine = Web3.to_checksum_address('0x078540eECC8b6d89949c9C7d5e8E91eAb64f6696')

        self.enjoy_contract = self.web3.eth.contract(address=self.enjoy, abi=self.token_abi)
        self.imagine_contract = self.web3.eth.contract(address=self.imagine, abi=self.token_abi)

    @exception_handler('Mint nft for ENJOY')
    def mint_enjoy(self):
        quantity = random.randint(QUANTITY_NFT_31[0], QUANTITY_NFT_31[1])
        token_balance = self.from_wei(18, self.enjoy_contract.functions.balanceOf(self.address_wallet).call())
        if token_balance < quantity:
            logger.error('Not enough ENJOY on balance\n')
            return False

        allowance = self.enjoy_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < Web3.to_wei(100000, 'ether'):
            self.approve(self.enjoy, self.address)
            sleeping(5, 10)

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        with open("word.txt", "r") as f:
            words = [row.strip() for row in f if row.strip()]

        txn = self.contract.functions.mint(
            self.address_wallet,
            quantity,
            Web3.to_checksum_address('0x95257b644f6beca994f7e19a1e02f5f8086c8e6c'),
            1,
            Web3.to_wei(quantity, 'ether'),
            self.enjoy,
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C'),
            random.choice(words)
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} NFT')

    @exception_handler('Mint nft for Imagine')
    def mint_imagine(self):
        quantity = random.randint(QUANTITY_NFT_32[0], QUANTITY_NFT_32[1])
        token_balance = self.from_wei(18, self.imagine_contract.functions.balanceOf(self.address_wallet).call())
        if token_balance < quantity:
            logger.error('Not enough Imagine on balance\n')
            return False

        allowance = self.imagine_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < Web3.to_wei(100000, 'ether'):
            self.approve(self.imagine, self.address)
            sleeping(5, 10)

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        with open("word.txt", "r") as f:
            words = [row.strip() for row in f if row.strip()]

        txn = self.contract.functions.mint(
            self.address_wallet,
            quantity,
            Web3.to_checksum_address('0xd202237ad529ac6d8f21f6b426d080f61cf5450f'),
            2,
            10000000 * quantity,
            self.imagine,
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C'),
            random.choice(words)
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} NFT')
