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
    {"address": "0xdB123EeDcFE960a03310D3A26f4A28D26627dcfe", "quantity": 5},
    {"address": "0x6B81dB6AdC67fd5E5C418cECbaBe0b308aBdb336", "quantity": 3},
    {"address": "0xBEB84aFE342fd6bEB2299B1a4F5d2bc28c4f4840", "quantity": 1},
    {"address": "0x96a420b4c68d12324a66d78780D6d3f1305358f8", "quantity": 3},
    {"address": "0x041D54c20cE67959eF5b0FE9fb23e3BEdFdFb2b3", "quantity": 1},
    {"address": "0x7854cF3526795825de031cdf494e1364a04e9538", "quantity": 2},
    {"address": "0xf75881b3cd35af9FDcF251A8c8a8158EC7f4a3C8", "quantity": 10},
    {"address": "0x1F781d47cD59257D7AA1Bd7b2fbaB50D57AF8587", "quantity": 1},
    {"address": "0x4fdD1f24238319dceAA8B3F514B4FdB3b6281CB0", "quantity": 3},
    {"address": "0xA85B9F9154db5bd9C0b7F869bC910a98ba1b7A87", "quantity": 3},
    {"address": "0x1e385327274b2EC5Ac1753f2E437EBd4E18b844d", "quantity": 10},
    {"address": "0xE4a39cAff4b4a85484191dCC122a55AE103C0039", "quantity": 2},
    {"address": "0x5c68EFfd0807ff3173c230de202186A0212180C4", "quantity": 1},
    {"address": "0xE8C87E2301a4479De2f4467F9b61B0b66192D033", "quantity": 1},
    {"address": "0x1828e1D65c06c16c2226652D3294d20Eac03c341", "quantity": 10},
    {"address": "0x26d35052D2D6f552cF9FCb811A7c742C587a196f", "quantity": 3},
    {"address": "0x695DF91CdCc9f0adDA1e5B2cEF66F0634cCe1D31", "quantity": 10},
    {"address": "0xC6835596743F076351AbAC0aa99ACCEed7429271", "quantity": 3},
    {"address": "0x5CB3Be6681E5aF9644F5356EbbaEE55BfCF86222", "quantity": 100},
    {"address": "0x8281e66fdB2F1Aa013f2D7B9e05C9BF7BD15A054", "quantity": 5},
    {"address": "0x0b88A7d17F25DaFC4e1856f255C23621C202CE43", "quantity": 1},
    {"address": "0x199A21f0be1cdcdd882865E7d0F462e4778c5ee4", "quantity": 2},
    {"address": "0x01dE72ABDE4F06D95784cfB90015FdF586b1e8B2", "quantity": 1},
    {"address": "0x6B1Af53f5Fb0F483e1FB218252cb0214E9B5f1FE", "quantity": 1},
    {"address": "0x669d7E515cc0a9eD60227B058C3E08f836843373", "quantity": 1}
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
