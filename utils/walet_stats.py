from utils.wallet import Wallet
import requests
import pandas as pd
from utils.retry import exception_handler
from web3 import Web3
from utils.func import crypto_prices

ETH_PRICE = crypto_prices['ethereum']


class ZoraScan(Wallet):
    def __init__(self, private_key, number, proxy):
        super().__init__(private_key, 'Zora', number, proxy)

    @exception_handler
    def get_nft_data(self):

        with requests.Session() as sess:
            if self.proxy is not None:
                proxy_dick = {'https': 'http://' + self.proxy, 'http': 'http://' + self.proxy}
                sess.proxies = proxy_dick
            resp = sess.get(f'https://explorer.zora.energy/api/v2/addresses/{self.address_wallet}/tokens')
            data = resp.json()
            wallet_info = {
                'Wallet Address': self.address_wallet,
                'Balance ETH': round(Web3.from_wei(self.get_native_balance(), 'ether'), 5),
                'Balance ETH in USD': round(float(round(Web3.from_wei(self.get_native_balance(), 'ether'), 5)) * ETH_PRICE, 3),
                'Tx Count': self.web3.eth.get_transaction_count(self.address_wallet),
                'Total NFT'    : 0,
                'ERC 721'      : 0,
                'ERC 1155'     : 0,
                'Name NFT ERC 721'     : [],
                'Quantity NFT ERC 721' : [],
                'Name NFT ERC 1155'    : [],
                'Quantity NFT ERC 1155': [],
            }

            for item in data['items']:
                token_type = item['token']['type']
                if token_type == 'ERC-721':
                    wallet_info['ERC 721'] += int(item['value'])
                    wallet_info['Name NFT ERC 721'].append(item['token']['name'])
                    wallet_info['Quantity NFT ERC 721'].append(int(item['value']))
                elif token_type == 'ERC-1155':
                    wallet_info['ERC 1155'] += int(item['value'])
                    wallet_info['Name NFT ERC 1155'].append(item['token']['name'])
                    wallet_info['Quantity NFT ERC 1155'].append(int(item['value']))

            wallet_info['Total NFT'] = wallet_info['ERC 721'] + wallet_info['ERC 1155']
        return wallet_info

    @staticmethod
    def save_to_exel(wallet_info_list):
        for wallet in wallet_info_list:
            for key in ['Name NFT ERC 721', 'Quantity NFT ERC 721', 'Name NFT ERC 1155', 'Quantity NFT ERC 1155']:
                wallet[key] = '\n'.join(map(str, wallet[key]))

        df1 = pd.DataFrame(wallet_info_list)
        df1.to_excel("./data/result.xlsx", index=False)
