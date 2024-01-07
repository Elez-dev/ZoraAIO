from utils.chain import *

EXCEL_PASSWORD  = False    # Если ставите пароль на Exel с приватниками || True/ False
SHUFFLE_WALLETS = False    # Перемешка кошельков || True/ False

CHAIN_RPC = {
    'Arbitrum': 'https://1rpc.io/arb',
    'Optimism': 'https://1rpc.io/op',
    'Polygon' : 'https://1rpc.io/matic',
    'Zora'    : 'https://rpc.zora.energy',
    'Ethereum': 'https://rpc.ankr.com/eth',
    'Base'    : 'https://rpc.ankr.com/base'
}

MAX_GAS_ETH = 200                     # gas в gwei (смотреть здесь : https://etherscan.io/gastracker)
ZORA_GASPRICE_PRESCALE = 0.00006      # Использовать Max base fee и Priority fee для газа в Zora, экономия 0.3-0.5$
BASE_GASPRICE_PRESCALE = 0.1          # Использовать Max base fee и Priority fee для газа в Base

RETRY = 5                         # Кол-во попыток при ошибках / фейлах
TIME_DELAY = [100, 200]           # Задержка после ТРАНЗАКЦИЙ  [min, max]
TIME_ACCOUNT_DELAY = [200, 300]   # Задержка между АККАУНТАМИ  [min, max]
TIME_DELAY_ERROR = [10, 20]       # Задержка при ошибках / фейлах [min, max]

# 1 - Официальный мост https://bridge.zora.energy/ -----------------------------------------------------------------------------------------------------------------------------------------------

OFF_ZORA_DEPOSIT = [0.001, 0.002, 5]  # Сумма для депозита [min, max, round_decimal]

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

NUMBER_TRANS_7 = [1, 1]  # Количество транзакций [min, max]

# 8 - Mint Custom NFT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

URL_CUSTOM_NFT = ['https://zora.co/collect/zora:0x81d226fb36ca785583e79e84312335d0e166d59b/1']  # https://zora.co/collect/zora:0x81d226fb36ca785583e79e84312335d0e166d59b/1 - нфт от гиткоина
                                                                                                # Минт любых других нфт на Zora.co (Будет рандомная из списка)
                                                                                                # Сюда пишем url нфт

# 10 - Send money yourself -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NUMBER_TRANS_YOURSELF = [1, 2]    # Количсетво транзакций самому себе [min, max]

# 12 - Custom routes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

routes = ['mint_opensea_zorb', 'update_nft_metadata', 'send_money_yourself']

routes_shuffle        = True                       # Перемешивает модули
time_delay_routes_min = 100                        # Минимальная и
time_delay_routes_max = 200                        # Максимальная задержка между модулями

          # Список доступных модулей
          # 'merkly_refuel',                        - Merkly refuel
          # 'zerius_refuel',                        - Zerius refuel
          # 'mint_zorb_zora'                        - Mint PYTHON ZORB в сети ZORA     (Базовая комиссия 0.000777 ETH)
          # 'mint_zorb_base'                        - Mint PYTHON ZORB в сети BASE     (Базовая комиссия 0.000777 ETH)
          # 'mint_zorb_optimism'                    - Mint PYTHON ZORB в сети OPTIMISM (Базовая комиссия 0.000777 ETH)
          # 'mint_opensea_zorb_zora'                - Mint PYTHON ZORB через OpenSea в сети ZORA     (FREE MINT)
          # 'mint_opensea_zorb_base'                - Mint PYTHON ZORB через OpenSea в сети BASE     (FREE MINT)
          # 'mint_opensea_zorb_optimism'            - Mint PYTHON ZORB через OpenSea в сети OPTIMISM (FREE MINT)
          # 'mint_custom_nft',                      - Mint Custon NFT
          # 'update_nft_metadata',                  - Update NFT metadata
          # 'send_money_yourself',                  - Send money yourself
