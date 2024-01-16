from utils.wallet import Wallet
from utils.retry import exception_handler
from web3 import Web3
import json as js
from loguru import logger


class ClaimReward(Wallet):

    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.address = Web3.to_checksum_address('0x7777777F279eba3d3Ad8F4E708545291A6fDBA8B')
        self.abi = js.load(open('./abi/claim_reward.txt'))
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    @exception_handler
    def claim(self):
        logger.info('Claim reward Zora.co')

        balance = self.contract.functions.balanceOf(self.address_wallet).call()
        if balance == 0:
            logger.error('Balance for claim - 0\n')
            return

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        txn = self.contract.functions.withdraw(
            self.address_wallet,
            balance
        ).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Claim {Web3.from_wei(balance, "ether")} ETH')
