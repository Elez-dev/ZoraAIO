from utils.wallet import Wallet
from loguru import logger
import json as js
from web3 import Web3
from eth_abi.packed import encode_packed
import random
from settings import VALUE_ZERIUS
from utils.retry import exception_handler


REFUEL_CONTRACTS = {
    'Optimism'      : Web3.to_checksum_address('0x2076BDd52Af431ba0E5411b3dd9B5eeDa31BB9Eb'),
    'Arbitrum'      : Web3.to_checksum_address('0x412aea168aDd34361aFEf6a2e3FC01928Fba1248'),
    'Polygon'       : Web3.to_checksum_address('0x2ef766b59e4603250265EcC468cF38a6a00b84b3'),
    'Base'          : Web3.to_checksum_address('0x9415AD63EdF2e0de7D8B9D8FeE4b939dd1e52F2C'),
    'Zora'          : Web3.to_checksum_address('0x1fe2c567169d39CCc5299727FfAC96362b2Ab90E')
}

contracts = {
    'Optimism': Web3.to_checksum_address('0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41'),
    'Polygon': Web3.to_checksum_address('0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41'),
    'Arbitrum': Web3.to_checksum_address('0x250c34D06857b9C0A036d44F86d2c1Abe514B3Da'),
    'Base': Web3.to_checksum_address('0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41'),
    'Zora': Web3.to_checksum_address('0x178608fFe2Cca5d36f3Fc6e69426c4D3A5A74A41')
}

lz_id_chain = {
    'Arbitrum': 110,
    'Optimism': 111,
    'Polygon': 109,
    'Base': 184,
    'Zora': 195
}


class Zerius(Wallet):

    def __init__(self, private_key, chain_from, chain_to, number, proxy):
        super().__init__(private_key, chain_from, number, proxy)
        self.abi_refuel = js.load(open('./abi/refuel_zerius.txt'))
        self.contract_refuel = self.web3.eth.contract(address=REFUEL_CONTRACTS[self.chain], abi=self.abi_refuel)

        self.abi_bridge = js.load(open('./abi/bridge_zerius.txt'))
        self.contract_bridge = self.web3.eth.contract(address=contracts[self.chain], abi=self.abi_bridge)

        self.chain_to = chain_to

    def get_nft_id(self):
        count = self.contract_bridge.functions.balanceOf(self.address_wallet).call()
        if count == 0:
            return 0
        tokens_arr = [self.contract_bridge.functions.tokenOfOwnerByIndex(self.address_wallet, i).call() for i in range(count)]
        return random.choice(tokens_arr)

    @exception_handler('Mint NFT on Zerius')
    def mint_nft(self):

        logger.info(f'Mint NFT {self.chain} on Zerius')

        contract_bridge = self.web3.eth.contract(address=contracts[self.chain], abi=self.abi_bridge)

        value = contract_bridge.functions.mintFee().call()
        dick = {
            'from': self.address_wallet,
            'value': value,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            **self.get_gas_price()
        }
        txn = contract_bridge.functions.mint(Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')).build_transaction(dick)

        self.send_transaction_and_wait(txn, f'Mint NFT {self.chain} on Zerius')

    @exception_handler('Bridge NFT on Zerius')
    def bridge_nft(self, token_id):
        logger.info(f'Bridge {token_id} NFT || {self.chain} -> {self.chain_to}')

        min_dst_gas = self.contract_bridge.functions.minDstGasLookup(lz_id_chain[self.chain_to], 1).call()

        if min_dst_gas == 0:
            logger.error(f'You cannot bridge on the {self.chain_to} network')
            raise ValueError

        adapter_params = encode_packed(
            ["uint16", "uint256"],
            [1, min_dst_gas]
        )

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

    @exception_handler('Zerius refuel')
    def refuel(self):
        logger.info(f'Zerius refuel from {self.chain} to {self.chain_to}')

        amount = Web3.to_wei(round(random.uniform(VALUE_ZERIUS[0], VALUE_ZERIUS[1]), VALUE_ZERIUS[2]), 'ether')

        min_dst_gas = self.contract_refuel.functions.minDstGasLookup(lz_id_chain[self.chain_to], 0).call()

        if REFUEL_CONTRACTS[self.chain_to] is None:
            logger.error(f'You cannot get refuel on the {self.chain_to} network')
            raise ValueError

        if min_dst_gas == 0:
            logger.error(f'You cannot get gas on the {self.chain_to} network')
            raise ValueError

        adapter_params = encode_packed(
            ["uint16", "uint256", "uint256", "address"],
            [2, min_dst_gas, amount, self.address_wallet]
        )

        dst_contract_address = encode_packed(["address"], [REFUEL_CONTRACTS[self.chain_to]])
        send_value = self.contract_refuel.functions.estimateSendFee(lz_id_chain[self.chain_to], dst_contract_address, adapter_params).call()

        contract_txn = self.contract_refuel.functions.refuel(
            lz_id_chain[self.chain_to],
            dst_contract_address,
            adapter_params
        ).build_transaction(
            {
                "from": self.address_wallet,
                "value": send_value[0],
                "nonce": self.web3.eth.get_transaction_count(self.address_wallet),
                ** self.get_gas_price()
            }
        )

        self.send_transaction_and_wait(contract_txn, f'Zerius refuel from {self.chain} to {self.chain_to}')