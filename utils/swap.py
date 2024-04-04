from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
from utils.func import sleeping
from settings import TOKEN_SWAP, VALUE_SWAP
import json as js
import random
from hexbytes import HexBytes
import time


class Uniswap(Wallet):
    def __init__(self, private_key, number, proxy):
        super().__init__(private_key, 'Zora', number, proxy)
        self.token_to_sold = None
        self.address = Web3.to_checksum_address('0x2986d9721a49838ab4297b695858af7f17f38014')

    @exception_handler('Buy token on Uniswap')
    def buy_token(self):
        token_to_buy = random.choice(TOKEN_SWAP)
        token_contract = self.web3.eth.contract(address=token_to_buy, abi=self.token_abi)
        toke_name = token_contract.functions.name().call()
        logger.info(f'Buy {toke_name} token on Uniswap')

        value = round(random.uniform(VALUE_SWAP[0], VALUE_SWAP[1]), VALUE_SWAP[2])
        value_wei = Web3.to_wei(value, 'ether')

        json = {
            'amount': str(value_wei),
            'configs': [{
                'enableFeeOnTransferFeeFetching': True,
                'enableUniversalRouter': True,
                'protocols': ['V3'],
                'recipient': self.address_wallet,
                'routingType': 'CLASSIC',
            }],
            'intent': 'quote',
            'sendPortionEnabled': False,
            'tokenIn': 'ETH',
            'tokenInChainId': 7777777,
            'tokenOut': token_to_buy,
            'tokenOutChainId': 7777777,
            'type': 'EXACT_INPUT',
        }
        url = 'https://api.swap.zora.energy/quote'
        data = self.get_api_call_data_post(url, json)
        tx = {
            'chainId': 7777777,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'from': self.address_wallet,
            'to': self.address,
            'data': data['quote']['methodParameters']['calldata'],
            'value': value_wei,
            **self.get_gas_price()
        }

        gas = int(self.web3.eth.estimate_gas(tx) * 1.3)
        tx.update({'gas': gas})

        self.send_transaction_and_wait(tx, f'Swap from {value} ETH to {round(float(data["quote"]["quoteDecimals"]), 4)} {toke_name}')

        self.token_to_sold = token_to_buy

    @exception_handler('Sold token on Uniswap')
    def sold_token(self):
        self.token_to_sold = '0xa6B280B42CB0b7c4a4F789eC6cCC3a7609A1Bc39'
        if self.token_to_sold is None:
            return False
        token_contract = self.web3.eth.contract(address=self.token_to_sold, abi=self.token_abi)
        token_name = token_contract.functions.name().call()
        token_decimal = token_contract.functions.decimals().call()

        token_balance = token_contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            logger.error('Token balance - 0\n')
            return False

        logger.info(f'Sold {token_name} token on Uniswap')

        allowance = token_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < token_balance:
            logger.info('Need Approve')
            self.approve(self.token_to_sold, self.address)
            sleeping(50, 70)

        json = {
            'amount': str(token_balance),
            'configs': [{
                'enableFeeOnTransferFeeFetching': True,
                'enableUniversalRouter': True,
                'protocols': ['V3'],
                'recipient': self.address_wallet,
                'routingType': 'CLASSIC',
            }],
            'intent': 'quote',
            'sendPortionEnabled': False,
            'tokenIn': self.token_to_sold,
            'tokenInChainId': 7777777,
            'tokenOut': 'ETH',
            'tokenOutChainId': 7777777,
            'type': 'EXACT_INPUT',
        }
        url = 'https://api.swap.zora.energy/quote'
        data = self.get_api_call_data_post(url, json)
        logger.info(data['quote']['methodParameters']['calldata'])
        tx = {
            'chainId': 7777777,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'from': self.address_wallet,
            'to': self.address,
            'data': data['quote']['methodParameters']['calldata'],
            **self.get_gas_price()
        }

        gas = int(self.web3.eth.estimate_gas(tx) * 1.3)
        tx.update({'gas': gas})

        # logger.info(f'Swap from {self.from_wei(token_decimal, token_balance)} {token_name} to {round(float(data["quote"]["quoteDecimals"]), 5)} ETH')

        self.send_transaction_and_wait(tx, f'Swap from {self.from_wei(token_decimal, token_balance)} {token_name} to {round(float(data["quote"]["quoteDecimals"]), 5)} ETH')


        self.token_to_sold = None
