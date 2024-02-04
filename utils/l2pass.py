from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
from eth_abi.packed import encode_packed
import random
from utils.retry import exception_handler

contracts = {
    'Optimism': Web3.to_checksum_address('0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222'),
    'Polygon': Web3.to_checksum_address('0x042002711e4d7A7Fc486742a85dBf096beeb0420'),
    'Arbitrum': Web3.to_checksum_address('0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222'),
    'Base': Web3.to_checksum_address('0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222'),
    'Zora': Web3.to_checksum_address('0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222')
}

lz_id_chain = {
    'Arbitrum': 110,
    'Optimism': 111,
    'Polygon': 109,
    'Base': 184,
    'Zora': 195
}


class L2Pass(Wallet):

    def __init__(self, private_key, chain_from, chain_to, number, proxy):
        super().__init__(private_key, chain_from, number, proxy)

        self.abi_bridge = js.load(open('./abi/l2pass.txt'))
        self.contract_bridge = self.web3.eth.contract(address=contracts[self.chain], abi=self.abi_bridge)

        self.chain_to = chain_to

    def get_nft_id(self):
        count = self.contract_bridge.functions.balanceOf(self.address_wallet).call()
        if count == 0:
            return 0
        tokens_arr = [self.contract_bridge.functions.tokenOfOwnerByIndex(self.address_wallet, i).call() for i in range(count)]
        return random.choice(tokens_arr)

    @exception_handler('Mint NFT on L2Pass')
    def mint_nft(self):

        logger.info(f'Mint NFT {self.chain} on L2Pass')

        contract_bridge = self.web3.eth.contract(address=contracts[self.chain], abi=self.abi_bridge)

        value = contract_bridge.functions.mintPrice().call()
        dick = {
            'from': self.address_wallet,
            'value': value,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }
        txn = contract_bridge.functions.mint(1).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint NFT {self.chain} on L2Pass')

    @exception_handler('Bridge NFT')
    def bridge_nft(self, token_id):
        logger.info(f'Bridge {token_id} NFT || {self.chain} -> {self.chain_to}')

        adapter_params = '0x00010000000000000000000000000000000000000000000000000000000000030d40'

        native_fee, _ = self.contract_bridge.functions.estimateSendFee(
            lz_id_chain[self.chain_to],
            self.address_wallet,
            token_id,
            False,
            adapter_params
        ).call()

        contract_txn = self.contract_bridge.functions.sendFrom(
                self.address_wallet,
                lz_id_chain[self.chain_to],
                self.address_wallet,
                token_id,
                self.address_wallet,
                '0x0000000000000000000000000000000000000000',
                adapter_params
            ).build_transaction(
                {
                    "from": self.address_wallet,
                    "value": native_fee,
                    "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
                    ** self.get_gas_price()
                }
            )

        self.send_transaction_and_wait(contract_txn, f'Bridge {token_id} NFT || {self.chain} -> {self.chain_to}')
