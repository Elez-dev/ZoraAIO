import random
import requests
from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
import json as js
import os
from settings import QUANTITY_NFT_6, QUANTITY_NFT_7, QUANTITY_NFT_8

ADDRESS = {
    'Zora': Web3.to_checksum_address('0x04E2516A2c207E84a1839755675dfd8eF6302F0a'),
    'Base': Web3.to_checksum_address('0xff8b0f870ff56870dc5abd6cb3e6e89c8ba2e062'),
    'Optimism': Web3.to_checksum_address('0x3678862f04290E565cCA2EF163BAeb92Bb76790C')
}

addr_nft = ['0xd3c48e966fe50eafeacd833194a8da22795ae5d8',
            '0xdd9b90deb027cbcdacea70eb87a19196d04c21fe',
            '0x5d4523babbbb8087cafd15cdcfaae3b7c5418ba5',
            '0x51ddb74ba7c41a961f7503007f8252433563eb29',
            '0xa6afbe046a67777ea28c3707f4827822d0737d98']


class MintNFT(Wallet):

    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.address_zora = Web3.to_checksum_address('0x00005EA00Ac477B1030CE78506496e8C2dE24bf5')
        self.address_base = Web3.to_checksum_address('0x00005EA00Ac477B1030CE78506496e8C2dE24bf5')
        self.address_optimism = Web3.to_checksum_address('0x00005EA00Ac477B1030CE78506496e8C2dE24bf5')
        self.abi_1155 = js.load(open('./abi/1155.txt'))
        self.abi_opensea = js.load(open('./abi/opensea.txt'))

    @exception_handler('Mint PYTHON ZORB on OpenSea || Zora chain')
    def mint_opensea_zorb_zora(self):
        quantity = random.randint(QUANTITY_NFT_7[0], QUANTITY_NFT_7[1])
        logger.info(f'Mint {quantity} PYTHON ZORB on OpenSea || Zora chain')

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        contract = self.web3.eth.contract(address=self.address_zora, abi=self.abi_opensea)
        txn = contract.functions.mintPublic(
            Web3.to_checksum_address(random.choice(addr_nft)),
            Web3.to_checksum_address('0x0000a26b00c1F0DF003000390027140000fAa719'),
            Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),
            quantity
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} PYTHON ZORB on OpenSea')

    @exception_handler('Mint PYTHON ZORB on OpenSea || Base chain')
    def mint_opensea_zorb_base(self):
        quantity = random.randint(QUANTITY_NFT_7[0], QUANTITY_NFT_7[1])
        logger.info(f'Mint {quantity} PYTHON ZORB on OpenSea || Base chain')

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        contract = self.web3.eth.contract(address=self.address_base, abi=self.abi_opensea)
        txn = contract.functions.mintPublic(
            Web3.to_checksum_address('0x92dFC144B8B897d36E980e6E29217201801A1C1e'),
            Web3.to_checksum_address('0x0000a26b00c1F0DF003000390027140000fAa719'),
            Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),
            quantity
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} PYTHON ZORB on OpenSea')

    @exception_handler('Mint PYTHON ZORB on OpenSea || Optimism chain')
    def mint_opensea_zorb_opt(self):
        quantity = random.randint(QUANTITY_NFT_7[0], QUANTITY_NFT_7[1])
        logger.info(f'Mint {quantity} PYTHON ZORB on OpenSea || Optimism chain')

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        contract = self.web3.eth.contract(address=self.address_optimism, abi=self.abi_opensea)
        txn = contract.functions.mintPublic(
            Web3.to_checksum_address('0x4301db4122dc1058df3e0e09415d025467348cb1'),
            Web3.to_checksum_address('0x0000a26b00c1F0DF003000390027140000fAa719'),
            Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),
            quantity
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} PYTHON ZORB on OpenSea')

    @exception_handler('Mint PYTHON ZORB || Zora chain')
    def mint_zorb_zora(self):
        quantity = random.randint(QUANTITY_NFT_6[0], QUANTITY_NFT_6[1])
        logger.info(f'Mint {quantity} PYTHON ZORB || Zora chain')

        contract = self.web3.eth.contract(address=Web3.to_checksum_address('0xC94AcD65b6965370eBEf0a2AdCDAD5B4362dD671'), abi=self.abi_1155)
        fee = contract.functions.mintFee().call() * quantity
        dick = {
            'from': self.address_wallet,
            'value': fee,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        txn = contract.functions.mintWithRewards(
            Web3.to_checksum_address('0x04E2516A2c207E84a1839755675dfd8eF6302F0a'),
            1,
            quantity,
            '0x000000000000000000000000' + self.address_wallet[2:],
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} PYTHON ZORB')

    @exception_handler('Mint {quantity} PYTHON ZORB || Base chain')
    def mint_zorb_base(self):
        quantity = random.randint(QUANTITY_NFT_6[0], QUANTITY_NFT_6[1])
        logger.info(f'Mint {quantity} PYTHON ZORB || Base chain')

        contract = self.web3.eth.contract(address=Web3.to_checksum_address('0xd63A68fAf5dD0CE2C36Fd0D4B731b2889bD04952'), abi=self.abi_1155)
        fee = contract.functions.mintFee().call() * quantity
        dick = {
            'from': self.address_wallet,
            'value': fee,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        txn = contract.functions.mintWithRewards(
            Web3.to_checksum_address('0xff8b0f870ff56870dc5abd6cb3e6e89c8ba2e062'),
            1,
            quantity,
            '0x000000000000000000000000' + self.address_wallet[2:],
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} PYTHON ZORB')

    @exception_handler('Mint PYTHON ZORB || Optimism chain')
    def mint_zorb_opt(self):
        quantity = random.randint(QUANTITY_NFT_6[0], QUANTITY_NFT_6[1])
        logger.info(f'Mint {quantity} PYTHON ZORB || Optimism chain')

        contract = self.web3.eth.contract(address=Web3.to_checksum_address('0xcb4927957d33b0714a206721c0361638c2fc5f42'), abi=self.abi_1155)
        fee = contract.functions.mintFee().call() * quantity
        dick = {
            'from': self.address_wallet,
            'value': fee,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        txn = contract.functions.mintWithRewards(
            Web3.to_checksum_address('0x3678862f04290E565cCA2EF163BAeb92Bb76790C'),
            1,
            quantity,
            '0x000000000000000000000000' + self.address_wallet[2:],
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} PYTHON ZORB')

    @exception_handler('Mint Custom NFT')
    def mint_1155(self, address, nft_id):
        quantity = random.randint(QUANTITY_NFT_8[0], QUANTITY_NFT_8[1])
        logger.info(f'Mint {quantity} Custom NFT || {address}')
        contract = self.web3.eth.contract(address=Web3.to_checksum_address(address), abi=self.abi_1155)
        fee = contract.functions.mintFee().call() * quantity
        dick = {
            'from': self.address_wallet,
            'value': fee,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }
        name = contract.functions.name().call()

        txn = contract.functions.mintWithRewards(
            ADDRESS[self.chain],
            int(nft_id),
            quantity,
            '0x000000000000000000000000' + self.address_wallet[2:],
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint {quantity} {name} NFT')

    @exception_handler('Update metadata NFT')
    def update_metadata(self, address):

        logger.info(f'Update metadata NFT || {address}')
        contract = self.web3.eth.contract(address=Web3.to_checksum_address(address), abi=self.abi_1155)
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
