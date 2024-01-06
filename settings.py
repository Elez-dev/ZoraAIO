from utils.chain import *

EXCEL_PASSWORD  = False    # Если ставите пароль на Exel с приватниками || True/ False
SHUFFLE_WALLETS = False    # Перемешка кошельков || True/ False

CHAIN_RPC = {
    'Arbitrum': 'https://1rpc.io/arb',
    'Optimism': 'https://1rpc.io/op',
    'Polygon' : 'https://1rpc.io/matic',
    'Zora'    : 'https://rpc.zora.energy',
    'Ethereum': 'https://rpc.ankr.com/eth'
}

MAX_GAS_ETH = 200                     # gas в gwei (смотреть здесь : https://etherscan.io/gastracker)
ZORA_GASPRICE_PRESCALE = 0.00006      # Использовать Max base fee и Priority fee для газа в Zora, экономия 0.3-0.5$


RETRY = 5                         # Кол-во попыток при ошибках / фейлах
TIME_DELAY = [100, 200]           # Задержка после ТРАНЗАКЦИЙ  [min, max]
TIME_ACCOUNT_DELAY = [200, 300]   # Задержка между АККАУНТАМИ  [min, max]
TIME_DELAY_ERROR = [10, 20]       # Задержка при ошибках / фейлах [min, max]

# 1 - Официальный мост https://bridge.zora.energy/ -----------------------------------------------------------------------------------------------------------------------------------------------

OFF_ZORA_DEPOSIT = [0.001, 0.002, 5]  # Сумма для депозита [min, max, decimal]

# 2 - Merkly ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_MERKLY = Optimism
CHAIN_TO_MERKLY   = Zora
VALUE_MERKLY      = [0.0035, 0.0035, 4]  # [min, max, round_decimal]

# 3 - Zerius -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_ZERIUS = Optimism           # Из какой сети
CHAIN_TO_ZERIUS   = Zora               # В какую сеть
VALUE_ZERIUS = [0.0035, 0.0035, 4]     # Количество [min, max, round_decimal]

CHAIN_TO_BRIDGE_ZERIUS = Polygon       # В какую сеть бридж нфт

# 7 - Mint PYTHON ZORB (Opensea) -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NUMBER_TRANS_7 = [1, 2]  # Количество транзакций [min, max]

# 8 - Mint Custom NFT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ADDRESS_CUSTOM_NFT = ['0x9b6f0450145c33067b1c16867d5b606dc6343132']  # Минт любых других нфт на Zora.co (Будет рандомная из списка)

# 10 - Send money yourself -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NUMBER_TRANS_YOURSELF = [1, 2]    # Количсетво транзакций самому себе [min, max]

# 12 - Custom routes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

routes = ['mint_opensea_zorb', 'update_nft_metadata', 'send_money_yourself']

routes_shuffle        = True                       # Перемешивает модули
time_delay_routes_min = 100                         # Минимальная и
time_delay_routes_max = 200                         # Максимальная задержка между модулями

          # Список доступных модулей
          # 'merkly_refuel',                        - Merkly refuel
          # 'zerius_refuel',                        - Zerius refuel
          # 'mint_bridge_nft',                      - Mint + Bridge NFT Zerius
          # 'mint_zorb',                            - Mint Python ZORB (ZORA)
          # 'mint_opensea_zorb',                    - Mint Python ZORB (Opensea)
          # 'mint_custom_nft',                      - Mint Custon NFT
          # 'update_nft_metadata',                  - Update NFT metadata
          # 'send_money_yourself',                  - Send money yourself
