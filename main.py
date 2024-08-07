import random
from loguru import logger
import sys
import time
from web3 import Web3
from utils import *
from utils.custom_route import CustomRouter
import requests
import json
from settings import *

logger.remove()
logger.add("./data/log.txt")
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <7}</level> | <cyan>{message}</cyan>")
web3_eth = Web3(Web3.HTTPProvider(CHAIN_RPC[Ethereum], request_kwargs={'timeout': 60}))

chain_list = {
    'zora' : Zora,
    'base' : Base,
    'oeth' : Optimism,
    'arb'  : Arbitrum,
    'blast': Blast
}


class Worker:
    def __init__(self, actoin):
        self.action = actoin

    @staticmethod
    def change_ip():
        try:
            res = requests.get(MOBILE_CHANGE_IP_LINK)
            logger.info(res.text)
        except Exception as error:
            logger.error(error)

    @staticmethod
    def generate_route():
        dick = {}
        for number, account in keys_list:
            key, proxy, address_nft, mail = account
            address = web3_eth.eth.account.from_key(key).address
            if routes_shuffle is True:
                random.shuffle(routes)

            new_routes = []

            for subarray in routes:
                if isinstance(subarray, list):
                    new_routes.append(random.choice(subarray))
                elif isinstance(subarray, str):
                    new_routes.append(subarray)
                else:
                    new_routes.append(None)

            dick[address] = {
                'index': 0,
                'route': new_routes
            }

        with open('./data/router.json', 'w') as f:
            json.dump(dick, f)

        logger.success('Successfully generated route\n')

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

        i = 0
        wallet_info_list = []
        for number, account in keys_list:
            str_number = f'{number} / {all_wallets}'
            key, proxy, address_nft, mail = account
            if MOBILE_PROXY is True:
                proxy = MOBILE_DATA
            i += 1
            address = web3_eth.eth.account.from_key(key).address
            logger.info(f'Account #{i} || {address}\n')

            if self.action == 1:
                dep = ZoraBridge(key, str_number)
                dep.bridge()

            if self.action == 2:
                bridge = TunnelBridge(key, CHAIN_FROM_TUNNEL, CHAIN_TO_TUNNEL, str_number, proxy)
                bridge.bridge()

            if self.action == 3:
                wr = WrapETH(key, Zora, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_9[0], NUMBER_TRANS_9[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    wr.wrap()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 4:
                wr = WrapETH(key, Zora, str_number, proxy)
                wr.unwrap()

            if self.action == 5:
                uniswap = Uniswap(key, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_11[0], NUMBER_TRANS_11[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    uniswap.buy_token()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])
                    uniswap.sold_token()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 6:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_zora()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 7:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Base, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_base()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 8:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Optimism, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_opt()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 9:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Blast, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_blast()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 10:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Arbitrum, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_arbitrum()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 11:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_opensea_zorb_zora()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 12:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Base, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_opensea_zorb_base()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 13:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Optimism, str_number, proxy)
                for _ in range(number_trans):
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
                clm = ClaimReward(key, Zora, str_number, proxy)
                clm.claim()

            if self.action == 20:
                wal = Wallet(key, Zora, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_YOURSELF[0], NUMBER_TRANS_YOURSELF[1])
                logger.info(f'Number of transactions to yourself - {number_trans}\n')
                for _ in range(number_trans):
                    wal.transfer_native(address)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 21:
                set_mail = SetEmail(key, str_number, proxy)
                set_mail.link_email(mail)

            if self.action == 22:
                crt = DeployContract(key, Zora, str_number, proxy)
                crt.create_contarct()

            if self.action == 23:
                zora = ZoraScan(key, str_number, proxy)
                wallet_info_list.append(zora.get_nft_data())
                time.sleep(0.5)
                continue

            if self.action == 24:
                uniswap = Uniswap(key, str_number, proxy)
                uniswap.buy_token()

            if self.action == 25:
                uniswap = Uniswap(key, str_number, proxy)
                res = uniswap.sold_token()
                if res is False:
                    continue

            if self.action == 26:
                nft = MintForEnjoy(key, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_31[0], NUMBER_TRANS_31[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    res = nft.mint_enjoy()
                    if res is False:
                        break
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 27:
                nft = MintForEnjoy(key, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_32[0], NUMBER_TRANS_32[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    res = nft.mint_imagine()
                    if res is False:
                        break
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 29:

                rout = CustomRouter(key, str_number, proxy, address_nft, address)
                res = rout.run()
                if res is False:
                    continue

            logger.success(f'Account completed, sleep and move on to the next one\n')
            sleeping(TIME_ACCOUNT_DELAY[0], TIME_ACCOUNT_DELAY[1])

            if MOBILE_PROXY is True:
                self.change_ip()

        if self.action == 23:
            ZoraScan.save_to_exel(wallet_info_list)
            return logger.success('The results are recorded in data/result.xlsx\n')


if __name__ == '__main__':
    list1 = get_accounts_data()
    logger.info(list1)
    all_wallets = len(list1)
    logger.info(f'Number of wallets: {all_wallets}\n')
    keys_list = shuffle(list1)

    while True:
        while True:
            logger.info('''
1  - OFFICIAL BRIDGE ETH -> ZORA
2  - INSTANT BRIDGE

3  - WRAP ETH
4 - UNWRAP ETH 
5 - BUY + SOLD TOKEN

6 - MINT NFT в сети ZORA             (С официальной комиссией ZORA 0.000777 ETH)
7 - MINT NFT в сети BASE             (С официальной комиссией ZORA 0.000777 ETH)
8 - MINT NFT в сети OPTIMISM         (С официальной комиссией ZORA 0.000777 ETH)
9 - MINT NFT в сети BLAST            (С официальной комиссией ZORA 0.000777 ETH)
10 - MINT NFT в сети ARBITRUM         (С официальной комиссией ZORA 0.000777 ETH)

11 - MINT NFT OPENSEA в сети ZORA     (FREE MINT)
12 - MINT NFT OPENSEA в сети BASE     (FREE MINT)
13 - MINT NFT OPENSEA в сети OPTIMISM (FREE MINT)

14 - MINT Custom NFT                  (ZORA.CO)
15 - MINT NFTS2ME                     (FREE MINT)
16 - MINT NFT FROM MINT.FUN           (FREE MINT)
17 - CREATE ERC1155 NFT CONTRACT      (ZORA.CO)
18 - UPDATE NFT METADATA              (ZORA.CO)
19 - CLAIM REWARD                     (ZORA.CO)
20 - SEND ETH YOURSELF
21 - SET EMAIL ON ZORA
22 - DEPLOY MERKLY CONTRACT
23 - CHECK WALLETS STATS
24 - BUY TOKEN
25 - SOLD TOKEN
26 - MINT NFT FOR $ENJOY              (ZORA.CO)
27 - MINT NFT FOR $IMAGINE            (ZORA.CO)

28 - GENERATE CUSTOM ROUTES           (сначала этот модуль -> потом 29)
29 - RUN CUSTOM ROUTES
''')

            time.sleep(0.1)
            act = int(input('Choose an action: '))

            if act == 28:
                Worker.generate_route()
                continue

            if act in range(1, 30):
                break

        worker = Worker(act)
        worker.work()
