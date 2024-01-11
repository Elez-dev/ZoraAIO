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
from utils.create_contract import CreateContract
from utils.l2pass import L2Pass
from utils.nft2me import NFT2ME
from utils.mintfun import MintFun


logger.remove()
logger.add("./data/log.txt")
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>")
web3_eth = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth', request_kwargs={'timeout': 60}))

chain_list = {
    'zora': Zora,
    'base': Base,
    'oeth': Optimism
}


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

    @staticmethod
    def get_chain_and_address():
        url = random.choice(URL_CUSTOM_NFT)
        if url.startswith('https://'):
            url = url[8:]
        if url.startswith('zora.co/collect/'):
            url = url[16:]
        chain, nft_info = tuple(url.split(':'))
        if '/' in nft_info:
            nft_address, token_id = tuple(nft_info.split('/'))
        else:
            nft_address, token_id = nft_info, 1

        return chain_list[chain], nft_address, token_id

    def work(self):

        self.get_chain_and_address()

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
                l2 = L2Pass(key, Zora, CHAIN_TO_BRIDGE_L2, str_number, proxy)
                l2.mint_nft()

            if self.action == 7:
                l2 = L2Pass(key, Zora, CHAIN_TO_BRIDGE_L2, str_number, proxy)
                nft_id = l2.get_nft_id()
                l2.bridge_nft(nft_id)

            if self.action == 8:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_zora()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 9:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Base, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_base()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 10:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Optimism, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_opt()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 11:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    zora.mint_opensea_zorb_zora()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 12:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Base, str_number, proxy)
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    zora.mint_opensea_zorb_base()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 13:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Optimism, str_number, proxy)
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    zora.mint_opensea_zorb_opt()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 14:
                number_trans = random.randint(NUMBER_TRANS_8[0], NUMBER_TRANS_8[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    chain, add, id_nft = self.get_chain_and_address()
                    zora = MintNFT(key, chain, str_number, proxy)
                    zora.mint_1155(add, id_nft)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 15:
                number_trans = random.randint(NUMBER_TRANS_15[0], NUMBER_TRANS_15[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    zora = NFT2ME(key, Zora, str_number, proxy)
                    zora.mint()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 16:
                number_trans = random.randint(NUMBER_TRANS_16[0], NUMBER_TRANS_16[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                mintfun = MintFun(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    mintfun.mint()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 17:
                contr = CreateContract(key, Zora, str_number, proxy)
                contr.create_contarct()

            if self.action == 18:
                if address_nft is None:
                    logger.error('Address NFT is empty\n')
                    continue
                zora = MintNFT(key, Zora, str_number, proxy)
                res = zora.update_metadata(address_nft)
                if res is False:
                    continue

            if self.action == 19:
                wal = Wallet(key, Zora, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_YOURSELF[0], NUMBER_TRANS_YOURSELF[1])
                logger.info(f'Number of transactions to yourself - {number_trans}\n')
                for _ in range(number_trans):
                    self.chek_gas_eth()
                    wal.transfer_native(address)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 20:
                zora = ZoraScan(key, str_number, proxy)
                wallet_info_list.append(zora.get_nft_data())
                time.sleep(0.1)
                continue

            if self.action == 21:

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

        if self.action == 20:
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
1  - Official Bridge ETH -> Zora
2  - Merkly GAS
3  - Zerius GAS
4  - Mint NFT Zerius
5  - Bridge NFT Zerius
6  - Mint NFT L2PASS
7  - Bridge NFT L2PASS 
8  - Mint PYTHON ZORB в сети ZORA     (С официальной комиссией ZORA 0.000777 ETH)
9  - Mint PYTHON ZORB в сети BASE     (С официальной комиссией ZORA 0.000777 ETH)
10 - Mint PYTHON ZORB в сети OPTIMISM (С официальной комиссией ZORA 0.000777 ETH)
11 - Mint PYTHON ZORB через OpenSea в сети ZORA     (FREE MINT)
12 - Mint PYTHON ZORB через OpenSea в сети BASE     (FREE MINT)
13 - Mint PYTHON ZORB через OpenSea в сети OPTIMISM (FREE MINT)
14 - Mint Custom NFT  (Zora.co)
15 - Mint NFTS2ME (FREE MINT)
16 - Mint free NFT from Mint.fun
17 - Create contract NFT ERC1155 (Zora.co)
18 - Update NFT metadata
19 - Send money yourself
20 - Check wallets stats
21 - Custom routs
''')

            time.sleep(0.1)
            act = int(input('Choose an action: '))

            if act in range(1, 22):
                break

        worker = Worker(act)
        worker.work()
