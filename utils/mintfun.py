import random
import requests
from loguru import logger
from web3 import Web3
from utils.wallet import Wallet
from utils.retry import exception_handler
import json as js

contracts = [
    {"address": "0x4de73D198598C3B4942E95657a12cBc399E4aDB5", "quantity": 1},
    {"address": "0x53cb0B849491590CaB2cc44AF8c20e68e21fc36D", "quantity": 3},
    {"address": "0x9eAE90902a68584E93a83D7638D3a95ac67FC446", "quantity": 3},
    {"address": "0x4073a52A3fc328D489534Ab908347eC1FcB18f7f", "quantity": 3},
    {"address": "0xC47ADb3e5dC59FC3B41d92205ABa356830b44a93", "quantity": 2},
    {"address": "0x8A43793D26b5DBd5133b78A85b0DEF8fB8Fce9B3", "quantity": 99},
    {"address": "0x266b7E8Df0368Dd4006bE5469DD4EE13EA53d3a4", "quantity": 3},
    {"address": "0xFa177a7eDC2518E70F8f8Ee159fA355D6b727257", "quantity": 3},
    {"address": "0x8974B96dA5886Ed636962F66a6456DC39118A140", "quantity": 3},
    {"address": "0xbC2cA61440fAF65a9868295Efa5d5D87c55B9529", "quantity": 4},
    {"address": "0xb096832A6ccD9053fe7a0EF075191Fe342D1AB75", "quantity": 2},
    {"address": "0x8f1B6776963bFcaa26f4e2a41289cFc3F50eD554", "quantity": 2},
    {"address": "0x93BCe2fF7CF7cFc722F70F8a5A93C2849C5eDEEF", "quantity": 2},
    {"address": "0x6BF820b6EF66B9946d078679a50DcDF2BF2e033c", "quantity": 4},
    {"address": "0x438F8f41801d470d0b7551F4d01853e7ca1fd0D8", "quantity": 5},
    {"address": "0x300Ee523E8b95B3B4DB763089505F525a2d61721", "quantity": 3},
    {"address": "0xdB123EeDcFE960a03310D3A26f4A28D26627dcfe", "quantity": 5}
  ]


class MintFun(Wallet):

    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)
        self.abi = js.load(open('./abi/mintfun.txt'))

    @exception_handler
    def mint(self):
        conract = random.choice(contracts)
        contr = self.web3.eth.contract(address=Web3.to_checksum_address(conract["address"]), abi=self.abi)
        name = contr.functions.name().call()
        logger.info(f'Mint {conract["quantity"]} {name} on MintFun || Zora chain')

        dick = {
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        contract_txn = contr.functions.mint(conract["quantity"]).build_transaction(dick)
        self.send_transaction_and_wait(contract_txn, f'Mint {conract["quantity"]} {name} on MintFun')
