from utils.wallet import Wallet
from utils.retry import exception_handler
from settings import ZORA_GASPRICE_PRESCALE
from web3 import Web3

class DeployContract(Wallet):

    def __init__(self, private_key, chain, number, proxy):
        super().__init__(private_key, chain, number, proxy)

    @exception_handler('Deploy contract')
    def create_contarct(self):
        tx = {
            'chainId': 7777777,
            'data': '0x60806040526000805461ffff1916905534801561001b57600080fd5b5060fb8061002a6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80630c55699c146037578063b49004e914605b575b600080fd5b60005460449061ffff1681565b60405161ffff909116815260200160405180910390f35b60616063565b005b60008054600191908190607a90849061ffff166096565b92506101000a81548161ffff021916908361ffff160217905550565b61ffff81811683821601908082111560be57634e487b7160e01b600052601160045260246000fd5b509291505056fea2646970667358221220666c87ec501268817295a4ca1fc6e3859faf241f38dd688f145135970920009264736f6c63430008120033',
            'from': self.address_wallet,
            'nonce': self.web3.eth.get_transaction_count(self.address_wallet),
            'gas': 150_000,
            **self.get_gas_price()
        }

        self.send_transaction_and_wait(tx, f'Deploy contract')



