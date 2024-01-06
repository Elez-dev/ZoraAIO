from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
from eth_abi import encode
from settings import VALUE_MERKLY
import random
from utils.retry import exception_handler

lz_id_chain = {
    'Arbitrum': 110,
    'Optimism': 111,
    'Polygon': 109,
    'Base': 184,
    'Zora': 195
}

contracts = {
    'Optimism': Web3.to_checksum_address('0xD7bA4057f43a7C4d4A34634b2A3151a60BF78f0d'),
    'Polygon': Web3.to_checksum_address('0x0E1f20075C90Ab31FC2Dd91E536e6990262CF76d'),
    'Arbitrum': Web3.to_checksum_address('0x4Ae8CEBcCD7027820ba83188DFD73CCAD0A92806'),
    'Base': Web3.to_checksum_address('0x6bf98654205B1AC38645880Ae20fc00B0bB9FFCA'),
    'Zora': Web3.to_checksum_address('0x461fcCF240CA4884Cc5413a5742F1bC56fAf7A0C')
}


class Merkly(Wallet):

    def __init__(self, private_key, chain_from, chain_to, number, proxy):
        super().__init__(private_key, chain_from, number, proxy)
        self.abi = js.load(open('./abi/refuel_merkly.txt'))
        self.chain_to = chain_to
        self.contract = self.web3.eth.contract(address=contracts[self.chain], abi=self.abi)

    @exception_handler
    def refuel(self):

        logger.info(f'Merkly refuel from {self.chain} to {self.chain_to}')
        amount = Web3.to_wei(round(random.uniform(VALUE_MERKLY[0], VALUE_MERKLY[1]), VALUE_MERKLY[2]), 'ether')
        amount_wei = Web3.to_hex(encode(["uint"], [amount]))
        adapter_params = "0x00020000000000000000000000000000000000000000000000000000000000030d40" + amount_wei[2:] + self.address_wallet[2:]
        send_value = self.contract.functions.estimateSendFee(lz_id_chain[self.chain_to], '0x', adapter_params).call()[0]

        dick = {
            'from': self.address_wallet,
            'value': int(send_value * 1.1),
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }

        contract_txn = self.contract.functions.bridgeGas(lz_id_chain[self.chain_to],
                                                         self.address_wallet,
                                                         adapter_params).build_transaction(dick)

        self.send_transaction_and_wait(contract_txn, f'Merkly refuel from {self.chain} to {self.chain_to}')
