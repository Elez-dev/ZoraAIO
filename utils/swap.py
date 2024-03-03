from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
from utils.func import sleeping
from settings import TOKEN_SWAP, VALUE_SWAP
import json as js
import random
import time


class Uniswap(Wallet):
    def __init__(self, private_key, number, proxy):
        super().__init__(private_key, 'Zora', number, proxy)
        self.address = Web3.to_checksum_address('0xa00F34A632630EFd15223B1968358bA4845bEEC7')
        self.abi = js.load(open('./abi/uniswap.txt'))
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        self.ETH = Web3.to_checksum_address('0x4200000000000000000000000000000000000006')
        self.token_to_sold = None

    def get_amount_out(self, token_to_buy, token_to_sold, value):
        amount_out = self.contract.functions.getAmountsOut(value, [token_to_sold, token_to_buy]).call()[1]
        return int(amount_out - (amount_out // 100))

    @exception_handler('Buy token on Uniswap')
    def buy_token(self):
        token_to_buy = random.choice(TOKEN_SWAP)
        token_contract = self.web3.eth.contract(address=token_to_buy, abi=self.token_abi)
        toke_name = token_contract.functions.name().call()
        logger.info(f'Buy {toke_name} token on Uniswap')

        value = round(random.uniform(VALUE_SWAP[0], VALUE_SWAP[1]), VALUE_SWAP[2])
        value_wei = Web3.to_wei(value, 'ether')

        min_tokens = self.get_amount_out(token_to_buy, self.ETH, value_wei)
        token_decimal = token_contract.functions.decimals().call()
        min_tok = self.from_wei(token_decimal, min_tokens)

        contract_txn = self.contract.functions.swapExactETHForTokens(
            min_tokens,
            [self.ETH, token_to_buy],
            self.address_wallet,
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': self.address_wallet,
            'value': value_wei,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        })

        self.send_transaction_and_wait(contract_txn, f'Buy {min_tok} {toke_name} Uniswap')

        self.token_to_sold = token_to_buy

    @exception_handler('Sold token on Uniswap')
    def sold_token(self):
        if self.token_to_sold is None:
            return
        token_contract = self.web3.eth.contract(address=self.token_to_sold, abi=self.token_abi)
        toke_name = token_contract.functions.name().call()
        logger.info(f'Sold {toke_name} token on Uniswap')

        token_balance = token_contract.functions.balanceOf(self.address_wallet).call()
        if token_balance == 0:
            return

        allowance = token_contract.functions.allowance(self.address_wallet, self.address).call()
        if allowance < token_balance:
            logger.info('Need Approve')
            self.approve(self.token_to_sold, self.address)
            sleeping(50, 70)

        min_tokens = self.get_amount_out(self.ETH, self.token_to_sold, token_balance)

        token_decimal = token_contract.functions.decimals().call()
        min_tok = self.from_wei(token_decimal, token_balance)

        contract_txn = self.contract.functions.swapExactTokensForETH(
            token_balance,
            min_tokens,
            [self.token_to_sold, self.ETH],
            self.address_wallet,
            (int(time.time()) + 10000)  # deadline
        ).build_transaction({
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        })

        self.send_transaction_and_wait(contract_txn, f'Sold {min_tok} {toke_name} Uniswap')

        self.token_to_sold = None
