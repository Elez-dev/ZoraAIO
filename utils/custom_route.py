from loguru import logger
from utils.func import get_accounts_data, shuffle
import sys
import time
from utils.func import sleeping
from web3 import Web3
from settings import *
from utils.off_bridge import ZoraBridge
from utils.merkly import Merkly
from utils.zerius import Zerius
from utils.mint_nft import MintNFT
from utils.wallet import Wallet
import random


class CustomRouter:

    def __init__(self, private_key, str_number, proxy, address_metadata, address_wallet):
        self.private_key = private_key
        self.str_number = str_number
        self.proxy = proxy
        self.address_metadata = address_metadata
        self.address_wallet = address_wallet

    def merkly_refuel(self):
        merkl = Merkly(self.private_key, CHAIN_FROM_MERKLY, CHAIN_TO_MERKLY, self.str_number, self.proxy)
        merkl.refuel()

    def zerius_refuel(self):
        zer = Zerius(self.private_key, CHAIN_FROM_ZERIUS, CHAIN_TO_ZERIUS, self.str_number, self.proxy)
        zer.refuel()

    def mint_bridge_nft(self):
        zer = Zerius(self.private_key, Zora, CHAIN_TO_BRIDGE_ZERIUS, self.str_number, self.proxy)
        zer.mint_nft()
        sleeping(TIME_ACCOUNT_DELAY[0], TIME_ACCOUNT_DELAY[1])
        nft_id = zer.get_nft_id()
        zer.bridge_nft(nft_id)

    def mint_zorb(self):
        zora = MintNFT(self.private_key, self.str_number, self.proxy)
        zora.mint_zorb()

    def mint_opensea_zorb(self):
        number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, self.str_number, self.proxy)
        zora.mint_opensea_zorb()

    def mint_custom_nft(self):
        zora = MintNFT(self.private_key, self.str_number, self.proxy)
        zora.mint_1155()

    def update_nft_metadata(self):
        if self.address_metadata is None:
            logger.error('Address NFT is empty\n')
            return
        zora = MintNFT(self.private_key, self.str_number, self.proxy)
        res = zora.update_metadata(self.address_metadata)
        if res is False:
            return

    def send_money_yourself(self):
        wal = Wallet(self.private_key, Zora, self.str_number, self.proxy)
        number_trans = random.randint(NUMBER_TRANS_YOURSELF[0], NUMBER_TRANS_YOURSELF[1])
        logger.info(f'Number of transactions to yourself - {number_trans}\n')
        for _ in range(number_trans):
            wal.transfer_native(self.address_wallet)
            sleeping(TIME_DELAY[0], TIME_DELAY[1])


