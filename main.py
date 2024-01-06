import random

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
from utils.walet_stats import ZoraScan
from utils.custom_route import CustomRouter


logger.remove()
logger.add("./data/log.txt")
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>")
web3_eth = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth', request_kwargs={'timeout': 60}))


class Worker:
    def __init__(self, actoin):
        self.action = actoin

    @staticmethod
    def chek_gas_eth():
        while True:
            try:
                res = int(round(Web3.from_wei(web3_eth.eth.gas_price, 'gwei')))
                logger.info(f'Газ сейчас - {res} gwei\n')
                if res <= MAX_GAS_ETH:
                    break
                else:
                    time.sleep(60)
                    continue
            except Exception as error:
                logger.error(error)
                time.sleep(30)
                continue

    def work(self):

        i = 0
        wallet_info_list = []
        for number, account in keys_list:
            str_number = f'{number} / {all_wallets}'
            key, proxy, address_nft = account
            i += 1
            address = web3_eth.eth.account.from_key(key).address
            logger.info(f'Account #{i} || {address}\n')
            self.chek_gas_eth()

            if self.action == 1:
                dep = ZoraBridge(key, str_number)
                dep.bridge()

            if self.action == 2:
                merkl = Merkly(key, CHAIN_FROM_MERKLY, CHAIN_TO_MERKLY, str_number, proxy)
                merkl.refuel()

            if self.action == 3:
                zer = Zerius(key, CHAIN_FROM_ZERIUS, CHAIN_TO_ZERIUS, str_number, proxy)
                zer.refuel()

            if self.action == 4:
                zer = Zerius(key, Zora, CHAIN_TO_ZERIUS, str_number, proxy)
                zer.mint_nft()

            if self.action == 5:
                zer = Zerius(key, Zora, CHAIN_TO_BRIDGE_ZERIUS, str_number, proxy)
                nft_id = zer.get_nft_id()
                zer.bridge_nft(nft_id)

            if self.action == 6:
                zora = MintNFT(key, str_number, proxy)
                zora.mint_zorb()

            if self.action == 7:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, str_number, proxy)
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    zora.mint_opensea_zorb()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 8:
                zora = MintNFT(key, str_number, proxy)
                zora.mint_1155()

            if self.action == 9:
                if address_nft is None:
                    logger.error('Address NFT is empty\n')
                    continue
                zora = MintNFT(key, str_number, proxy)
                res = zora.update_metadata(address_nft)
                if res is False:
                    continue

            if self.action == 10:
                wal = Wallet(key, Zora, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_YOURSELF[0], NUMBER_TRANS_YOURSELF[1])
                logger.info(f'Number of transactions to yourself - {number_trans}\n')
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    wal.transfer_native(address)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 11:
                zora = ZoraScan(key, str_number, proxy)
                wallet_info_list.append(zora.get_nft_data())
                time.sleep(0.1)
                continue

            if self.action == 12:

                rout = CustomRouter(key, str_number, proxy, address_nft, address)
                if routes_shuffle is True:
                    random.shuffle(routes)
                for method_name in routes:
                    logger.info(f'Module - {method_name}\n')
                    if hasattr(rout, method_name):
                        method = getattr(rout, method_name)
                        self.chek_gas_eth()
                        method()
                        logger.success(f'Module completed, sleep and move on to the next one\n')
                        sleeping(TIME_DELAY[0], TIME_DELAY[1])

            logger.success(f'Account completed, sleep and move on to the next one\n')
            sleeping(TIME_ACCOUNT_DELAY[0], TIME_ACCOUNT_DELAY[1])

        if self.action == 11:
            ZoraScan.save_to_exel(wallet_info_list)
            return logger.success('The results are recorded in data/result.xlsx\n')


if __name__ == '__main__':
    list1 = get_accounts_data()
    all_wallets = len(list1)
    logger.info(f'Number of wallets: {all_wallets}\n')
    keys_list = shuffle(list1)

    while True:
        while True:
            logger.info('''
1 - Official Bridge ETH -> Zora
2 - Merkly GAS
3 - Zerius GAS
4 - Mint NFT Zerius
5 - Bridge NFT Zerius
6 - Mint PYTHON ZORB (Zora.co)
7 - Mint PYTHON ZORB (Opensea)
8 - Mint Custom NFT  (Zora.co)
9 - Update NFT metadata
10 - Send money yourself
11 - Check wallets stats
12 - Custom routs
''')

            time.sleep(0.1)
            act = int(input('Choose an action: '))

            if act in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
                break

        worker = Worker(act)
        worker.work()
