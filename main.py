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
                merkl = Merkly(key, CHAIN_FROM_MERKLY, CHAIN_TO_MERKLY, str_number, proxy)
                merkl.refuel()

            if self.action == 4:
                zer = Zerius(key, CHAIN_FROM_ZERIUS, CHAIN_TO_ZERIUS, str_number, proxy)
                zer.refuel()

            if self.action == 5:
                zer = Zerius(key, Zora, CHAIN_TO_ZERIUS, str_number, proxy)
                zer.mint_nft()

            if self.action == 6:
                zer = Zerius(key, Zora, CHAIN_TO_BRIDGE_ZERIUS, str_number, proxy)
                nft_id = zer.get_nft_id()
                zer.bridge_nft(nft_id)

            if self.action == 7:
                l2 = L2Pass(key, Zora, CHAIN_TO_BRIDGE_L2, str_number, proxy)
                l2.mint_nft()

            if self.action == 8:
                l2 = L2Pass(key, Zora, CHAIN_TO_BRIDGE_L2, str_number, proxy)
                nft_id = l2.get_nft_id()
                l2.bridge_nft(nft_id)

            if self.action == 9:
                wr = WrapETH(key, Zora, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_9[0], NUMBER_TRANS_9[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    wr.wrap()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 10:
                wr = WrapETH(key, Zora, str_number, proxy)
                wr.unwrap()

            if self.action == 11:
                uniswap = Uniswap(key, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_11[0], NUMBER_TRANS_11[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    uniswap.buy_token()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])
                    uniswap.sold_token()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 12:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_zora()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 13:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Base, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_base()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 14:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Optimism, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_opt()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 15:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Blast, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_blast()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 16:
                number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Arbitrum, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_zorb_arbitrum()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 17:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_opensea_zorb_zora()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 18:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Base, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_opensea_zorb_base()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 19:
                number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                zora = MintNFT(key, Optimism, str_number, proxy)
                for _ in range(number_trans):
                    zora.mint_opensea_zorb_opt()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 20:
                number_trans = random.randint(NUMBER_TRANS_8[0], NUMBER_TRANS_8[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    chain, add, id_nft = self.get_chain_and_address()
                    zora = MintNFT(key, chain, str_number, proxy)
                    zora.mint_1155(add, id_nft)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 21:
                number_trans = random.randint(NUMBER_TRANS_15[0], NUMBER_TRANS_15[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                for _ in range(number_trans):
                    zora = NFT2ME(key, Zora, str_number, proxy)
                    zora.mint()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 22:
                number_trans = random.randint(NUMBER_TRANS_16[0], NUMBER_TRANS_16[1])
                logger.info(f'Number of transactions - {number_trans}\n')
                mintfun = MintFun(key, Zora, str_number, proxy)
                for _ in range(number_trans):
                    mintfun.mint()
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 23:
                contr = CreateContract(key, Zora, str_number, proxy)
                contr.create_contarct()

            if self.action == 24:
                if address_nft is None:
                    logger.error('Address NFT is empty\n')
                    continue
                zora = MintNFT(key, Zora, str_number, proxy)
                res = zora.update_metadata(address_nft)
                if res is False:
                    continue

            if self.action == 25:
                clm = ClaimReward(key, Zora, str_number, proxy)
                clm.claim()

            if self.action == 26:
                wal = Wallet(key, Zora, str_number, proxy)
                number_trans = random.randint(NUMBER_TRANS_YOURSELF[0], NUMBER_TRANS_YOURSELF[1])
                logger.info(f'Number of transactions to yourself - {number_trans}\n')
                for _ in range(number_trans):
                    wal.transfer_native(address)
                    sleeping(TIME_DELAY[0], TIME_DELAY[1])

            if self.action == 27:
                set_mail = SetEmail(key, str_number, proxy)
                set_mail.link_email(mail)

            if self.action == 28:
                crt = DeployContract(key, Zora, str_number, proxy)
                crt.create_contarct()

            if self.action == 29:
                zora = ZoraScan(key, str_number, proxy)
                wallet_info_list.append(zora.get_nft_data())
                time.sleep(0.5)
                continue

            if self.action == 31:

                rout = CustomRouter(key, str_number, proxy, address_nft, address)
                res = rout.run()
                if res is False:
                    continue

            logger.success(f'Account completed, sleep and move on to the next one\n')
            sleeping(TIME_ACCOUNT_DELAY[0], TIME_ACCOUNT_DELAY[1])

            if MOBILE_PROXY is True:
                self.change_ip()

        if self.action == 29:
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
2  - Relay bridge

3  - Merkly GAS
4  - Zerius GAS
5  - Mint NFT Zerius
6  - Bridge NFT Zerius
7  - Mint NFT L2PASS
8  - Bridge NFT L2PASS

9  - Wrap ETH
10 - Unwrap ETH 
11 - Buy + Sold token

12 - Mint NFT в сети ZORA        (С официальной комиссией ZORA 0.000777 ETH)
13 - Mint NFT в сети BASE        (С официальной комиссией ZORA 0.000777 ETH)
14 - Mint NFT в сети OPTIMISM    (С официальной комиссией ZORA 0.000777 ETH)
15 - Mint NFT в сети Blast       (С официальной комиссией ZORA 0.000777 ETH)
16 - Mint NFT в сети Arbitrum    (С официальной комиссией ZORA 0.000777 ETH)

17 - Mint NFT через OpenSea в сети ZORA     (FREE MINT)
18 - Mint NFT через OpenSea в сети BASE     (FREE MINT)
19 - Mint NFT через OpenSea в сети OPTIMISM (FREE MINT)

20 - Mint Custom NFT  (Zora.co)
21 - Mint NFTS2ME     (FREE MINT)
22 - Mint FREE NFT from Mint.fun
23 - Create contract NFT ERC1155 (Zora.co)
24 - Update NFT metadata
25 - Claim reward (Zora.co)
26 - Send money yourself
27 - Set email Zora.co
28 - Deploy Merkly contract
29 - Check wallets stats

30 - Generate Custom routes(сначала этот модуль -> потом 31)
31 - Run Custom routs
''')

            time.sleep(0.1)
            act = int(input('Choose an action: '))

            if act == 30:
                Worker.generate_route()
                continue

            if act in range(1, 32):
                break

        worker = Worker(act)
        worker.work()
