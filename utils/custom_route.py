from loguru import logger
from settings import *
from utils import *
from web3 import Web3
import random
import time
import json

web3_eth = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth', request_kwargs={'timeout': 60}))

chain_list = {
    'zora': Zora,
    'base': Base,
    'oeth': Optimism
}


class CustomRouter:

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

    def __init__(self, private_key, str_number, proxy, address_metadata, address_wallet):
        self.private_key = private_key
        self.str_number = str_number
        self.proxy = proxy
        self.address_metadata = address_metadata
        self.address_wallet = address_wallet

    def mint_zorb_zora(self):
        number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Zora, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_zorb_zora()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_zorb_base(self):
        number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Base, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_zorb_base()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_zorb_optimism(self):
        number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Optimism, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_zorb_opt()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_opensea_zorb_zora(self):
        number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Zora, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_opensea_zorb_zora()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_opensea_zorb_base(self):
        number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Base, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_opensea_zorb_base()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_opensea_zorb_optimism(self):
        number_trans = random.randint(NUMBER_TRANS_7[0], NUMBER_TRANS_7[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Optimism, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_opensea_zorb_opt()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_custom_nft(self):
        number_trans = random.randint(NUMBER_TRANS_8[0], NUMBER_TRANS_8[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        for _ in range(number_trans):
            chain, add, id_nft = self.get_chain_and_address()
            zora = MintNFT(self.private_key, chain, self.str_number, self.proxy)
            zora.mint_1155(add, id_nft)
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def update_nft_metadata(self):
        if self.address_metadata is None:
            logger.error('Address NFT is empty\n')
            return
        zora = MintNFT(self.private_key, Zora, self.str_number, self.proxy)
        zora.update_metadata(self.address_metadata)

    def send_money_yourself(self):
        wal = Wallet(self.private_key, Zora, self.str_number, self.proxy)
        number_trans = random.randint(NUMBER_TRANS_YOURSELF[0], NUMBER_TRANS_YOURSELF[1])
        logger.info(f'Number of transactions to yourself - {number_trans}\n')
        for _ in range(number_trans):
            wal.transfer_native(self.address_wallet)
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_nft2me(self):
        number_trans = random.randint(NUMBER_TRANS_15[0], NUMBER_TRANS_15[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = NFT2ME(self.private_key, Zora, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def create_contract(self):
        contr = CreateContract(self.private_key, Zora, self.str_number, self.proxy)
        contr.create_contarct()

    def mintfun(self):
        number_trans = random.randint(NUMBER_TRANS_16[0], NUMBER_TRANS_16[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        mintfun = MintFun(self.private_key, Zora, self.str_number, self.proxy)
        for _ in range(number_trans):
            mintfun.mint()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def wrap_unwrap(self):
        wr = WrapETH(self.private_key, Zora, self.str_number, self.proxy)
        number_trans = random.randint(NUMBER_TRANS_9[0], NUMBER_TRANS_9[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        for _ in range(number_trans):
            wr.wrap()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

        wr.unwrap()

    def swap(self):
        uniswap = Uniswap(self.private_key, self.str_number, self.proxy)
        number_trans = random.randint(NUMBER_TRANS_11[0], NUMBER_TRANS_11[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        for _ in range(number_trans):
            uniswap.buy_token()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])
            uniswap.sold_token()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_zorb_blast(self):
        number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Blast, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_zorb_blast()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_zorb_arbitrum(self):
        number_trans = random.randint(NUMBER_TRANS_6[0], NUMBER_TRANS_6[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        zora = MintNFT(self.private_key, Arbitrum, self.str_number, self.proxy)
        for _ in range(number_trans):
            zora.mint_zorb_arbitrum()
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def buy_token(self):
        uniswap = Uniswap(self.private_key, self.str_number, self.proxy)
        uniswap.buy_token()

    def mint_for_enjoy(self):
        nft = MintForEnjoy(self.private_key, self.str_number, self.proxy)
        number_trans = random.randint(NUMBER_TRANS_31[0], NUMBER_TRANS_31[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        for _ in range(number_trans):
            res = nft.mint_enjoy()
            if res is False:
                break
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def mint_for_imagine(self):
        nft = MintForEnjoy(self.private_key, self.str_number, self.proxy)
        number_trans = random.randint(NUMBER_TRANS_32[0], NUMBER_TRANS_32[1])
        logger.info(f'Number of transactions - {number_trans}\n')
        for _ in range(number_trans):
            res = nft.mint_imagine()
            if res is False:
                break
            sleeping(TIME_DELAY[0], TIME_DELAY[1])

    def run(self):

        address = web3_eth.eth.account.from_key(self.private_key).address
        try:
            data = json.load(open('./data/router.json'))
            route = data[address]['route']
            index = data[address]['index']
        except Exception as error:
            logger.error(error)
            return False

        flag = False

        while index < len(route):
            method_name = route[index]
            if method_name is None:
                index += 1
                continue
            if hasattr(self, method_name):
                logger.info(f'Module - {method_name}\n')
                if hasattr(self, method_name):
                    method = getattr(self, method_name)
                    try:
                        method()
                        logger.success(f'Module completed, sleep and move on to the next one\n')
                        sleeping(TIME_DELAY_ROUTES[0], TIME_DELAY_ROUTES[1])
                        flag = True
                    except Exception as error:
                        logger.error(error)
                        time.sleep(20)
                    finally:
                        index += 1
                        data[address]['index'] = index
                        with open('./data/router.json', 'w') as f:
                            json.dump(data, f)
        else:
            return flag


