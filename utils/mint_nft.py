import random
import requests
from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
import json as js
import os


class MintNFT(Wallet):

    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.address_zora = Web3.to_checksum_address('0x00005EA00Ac477B1030CE78506496e8C2dE24bf5')
        self.address_base = Web3.to_checksum_address('0x00005EA00Ac477B1030CE78506496e8C2dE24bf5')
        self.address_optimism = Web3.to_checksum_address('0x00005EA00Ac477B1030CE78506496e8C2dE24bf5')
        self.abi = js.load(open('./abi/1155.txt'))

    @exception_handler
    def mint_opensea_zorb_zora(self):
        logger.info('Mint PYTHON ZORB on OpenSea || Zora chain')

        txn = {
            'chainId': self.web3.eth.chain_id,
            'data': '0x161ac21f000000000000000000000000d3c48e966fe50eafeacd833194a8da22795ae5d80000000000000000000000000000a26b00c1f0df003000390027140000faa71900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001360c6ebe',
            'from': self.address_wallet,
            'to': self.address_zora,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 130_000,
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(txn, 'Mint PYTHON ZORB on OpenSea')

    @exception_handler
    def mint_opensea_zorb_base(self):
        logger.info('Mint PYTHON ZORB on OpenSea || Base chain')

        txn = {
            'chainId': self.web3.eth.chain_id,
            'data': '0x161ac21f00000000000000000000000092dfc144b8b897d36e980e6e29217201801a1c1e0000000000000000000000000000a26b00c1f0df003000390027140000faa71900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001360c6ebe',
            'from': self.address_wallet,
            'to': self.address_base,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 130_000,
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(txn, 'Mint PYTHON ZORB on OpenSea')

    @exception_handler
    def mint_opensea_zorb_opt(self):
        logger.info('Mint PYTHON ZORB on OpenSea || Optimism chain')

        txn = {
            'chainId': self.web3.eth.chain_id,
            'data': '0x161ac21f0000000000000000000000004301db4122dc1058df3e0e09415d025467348cb10000000000000000000000000000a26b00c1f0df003000390027140000faa71900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001360c6ebe',
            'from': self.address_wallet,
            'to': self.address_optimism,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 130_000,
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(txn, 'Mint PYTHON ZORB on OpenSea')

    @exception_handler
    def mint_zorb_zora(self):
        logger.info('Mint PYTHON ZORB || Zora chain')

        txn = {
            'chainId': self.web3.eth.chain_id,
            'data': '0x9dbb844d00000000000000000000000004e2516a2c207e84a1839755675dfd8ef6302f0a0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000cc05e5454d8ec8f0873ecd6b2e3da945b39aca6c0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000' + self.address_wallet[2:],
            'from': self.address_wallet,
            'to': Web3.to_checksum_address('0xC94AcD65b6965370eBEf0a2AdCDAD5B4362dD671'),
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 200_000,
            'value': Web3.to_wei(0.000777, 'ether'),
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(txn, 'Mint PYTHON ZORB')

    @exception_handler
    def mint_zorb_base(self):
        logger.info('Mint PYTHON ZORB || Base chain')

        txn = {
            'chainId': self.web3.eth.chain_id,
            'data': '0x9dbb844d000000000000000000000000ff8b0f870ff56870dc5abd6cb3e6e89c8ba2e0620000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000cc05e5454d8ec8f0873ecd6b2e3da945b39aca6c0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000' + self.address_wallet[2:],
            'from': self.address_wallet,
            'to': Web3.to_checksum_address('0xd63A68fAf5dD0CE2C36Fd0D4B731b2889bD04952'),
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 200_000,
            'value': Web3.to_wei(0.000777, 'ether'),
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(txn, 'Mint PYTHON ZORB')

    @exception_handler
    def mint_zorb_opt(self):
        logger.info('Mint PYTHON ZORB || Optimism chain')

        txn = {
            'chainId': self.web3.eth.chain_id,
            'data': '0x9dbb844d0000000000000000000000003678862f04290e565cca2ef163baeb92bb76790c0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000cc05e5454d8ec8f0873ecd6b2e3da945b39aca6c0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000' + self.address_wallet[2:],
            'from': self.address_wallet,
            'to': Web3.to_checksum_address('0xCB4927957D33B0714A206721c0361638C2Fc5f42'),
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 200_000,
            'value': Web3.to_wei(0.000777, 'ether'),
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(txn, 'Mint PYTHON ZORB')

    @exception_handler
    def mint_1155(self, address, nft_id):
        logger.info(f'Mint Custom NFT || {address}')
        contract = self.web3.eth.contract(address=Web3.to_checksum_address(address), abi=self.abi)
        fee = contract.functions.mintFee().call()
        dick = {
            'from': self.address_wallet,
            'value': fee,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }
        name = contract.functions.name().call()

        txn = contract.functions.mintWithRewards(
            Web3.to_checksum_address('0x04E2516A2c207E84a1839755675dfd8eF6302F0a'),
            nft_id,
            1,
            '0x000000000000000000000000cc05e5454d8ec8f0873ecd6b2e3da945b39aca6c',
            self.address_wallet
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {name} NFT')

    @exception_handler
    def update_metadata(self, address):

        logger.info(f'Update metadata NFT || {address}')
        contract = self.web3.eth.contract(address=Web3.to_checksum_address(address), abi=self.abi)
        owner = contract.functions.owner().call()
        if owner != self.address_wallet:
            logger.error(f'Сurrent wallet: {self.address_wallet} || Creater NFT: {owner}\n')
            return False

        picture_list = os.listdir('picture')
        file_list = []
        for picture in picture_list:
            with open(f'picture/{picture}', "rb") as f:
                file = f.read()
                file_list.append(file)
        pic = random.choice(file_list)

        files = {"file": pic}
        url = 'https://ipfs-uploader.zora.co/api/v0/add?stream-channels=true&cid-version=1&progress=false'
        res = requests.post(url=url, files=files, timeout=60)
        json_data = res.json()
        url_pictire = 'ipfs://' + json_data['Hash']

        with open('utils/words.txt', 'r') as f:
            list_word = f.readlines()
        word = random.choice(list_word)[:-1] + random.choice(list_word)[:-1]

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }
        txn = contract.functions.updateContractMetadata(url_pictire, word).build_transaction(dick)
        self.send_transaction_and_wait(txn, 'Update metadata NFT')
