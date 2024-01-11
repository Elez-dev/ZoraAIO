from utils.chain import *

EXCEL_PASSWORD  = False                            # Если ставите пароль на Excel с приватниками || True/ False
SHUFFLE_WALLETS = True                             # Перемешка кошельков                         || True/ False

CHAIN_RPC = {
    'Arbitrum': 'https://1rpc.io/arb',
    'Optimism': 'https://1rpc.io/op',
    'Polygon' : 'https://1rpc.io/matic',
    'Zora'    : 'https://rpc.zora.energy',
    'Ethereum': 'https://rpc.ankr.com/eth',
    'Base'    : 'https://rpc.ankr.com/base'
}

MAX_GAS_ETH = 40                                   # gas в gwei (смотреть здесь : https://etherscan.io/gastracker)
ZORA_GASPRICE_PRESCALE = 0.00006                   # Использовать Max base fee и Priority fee для газа в Zora, экономия 0.3-0.5$
BASE_GASPRICE_PRESCALE = 0.05                      # Использовать Max base fee и Priority fee для газа в Base

RETRY = 5                                          # Количество попыток при ошибках / фейлах
TIME_DELAY = [100, 200]                            # Задержка после ТРАНЗАКЦИЙ     [min, max]
TIME_ACCOUNT_DELAY = [200, 300]                    # Задержка между АККАУНТАМИ     [min, max]
TIME_DELAY_ERROR = [10, 20]                        # Задержка при ошибках / фейлах [min, max]

# 1 - Официальный мост https://bridge.zora.energy/ -----------------------------------------------------------------------------------------------------------------------------------------------

OFF_ZORA_DEPOSIT = [0.003, 0.003, 5]               # Сумма для депозита [min, max, round_decimal]
                                                   # Если сумма больше чем на балансе, будет бридж всего баланса

# 2 - Merkly ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_MERKLY = Optimism                       # Из какой сети
CHAIN_TO_MERKLY   = Zora                           # В какую сеть
VALUE_MERKLY      = [0.0075, 0.0075, 4]            # Количество [min, max, round_decimal]

# 3 - 5 || Zerius -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_ZERIUS = Optimism                       # Из какой сети
CHAIN_TO_ZERIUS   = Zora                           # В какую сеть
VALUE_ZERIUS = [0.003, 0.003, 4]                   # Количество [min, max, round_decimal]

CHAIN_TO_BRIDGE_ZERIUS = Base                      # В какую сеть бридж NFT

# 6 - 7 || L2PASS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CHAIN_TO_BRIDGE_L2 = Base                          # В какую сеть бридж NFT

# 8 - 10 || Mint PYTHON ZORB (Zora.co) --------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_6 = [1, 1]                            # Количество NFT для минта
NUMBER_TRANS_6 = [1, 1]                            # Количество транзакций             [min, max]

# 11 - 13 || Mint PYTHON ZORB (OpenSea) || FREE MINT -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_7 = [100, 700]                        # Количество NFT для минта
NUMBER_TRANS_7 = [1, 2]                            # Количество транзакций             [min, max]

# 14 - Mint Custom NFT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

URL_CUSTOM_NFT = ['https://zora.co/collect/zora:0x81d226fb36ca785583e79e84312335d0e166d59b/1',  # https://zora.co/collect/zora:0x81d226fb36ca785583e79e84312335d0e166d59b/1 - NFT от Gitcoin
                  'https://zora.co/collect/zora:0x1dc9ff62bbc4c6f2ed4ef3fbc095db5416e4894f/1',  # https://zora.co/collect/zora:0x1dc9ff62bbc4c6f2ed4ef3fbc095db5416e4894f/1 - Layer3 on Zora
                  'https://zora.co/collect/oeth:0x6995d9f4ab942dc5385e9b6986253ab22793e28f/1',  # https://zora.co/collect/oeth:0x6995d9f4ab942dc5385e9b6986253ab22793e28f/1 - Upload Imagination (OPTIMISM)
                  'https://zora.co/collect/zora:0x393c46fe7887697124a73f6028f39751aa1961a3/1',  # https://zora.co/collect/zora:0x393c46fe7887697124a73f6028f39751aa1961a3/1 - NFT от Co-founder Sound.xyz
                  'https://zora.co/collect/oeth:0xe538598941e4a25f471aef9b1b5dffd6ee0fda54/2',  # https://zora.co/collect/oeth:0xe538598941e4a25f471aef9b1b5dffd6ee0fda54/2 - THE WORLD OF ENDLESS POSSIBILITIES от Zerion Wallet (OPTIMISM)
                  'https://zora.co/collect/oeth:0x31eb3dd0e75dac10d07e8c6cfa54bcb7ae1774ce',    # https://zora.co/collect/oeth:0x31eb3dd0e75dac10d07e8c6cfa54bcb7ae1774ce   - WHY ARE YOU STILL HERE? от Zerion Wallet (OPTIMISM)
                  'https://zora.co/collect/zora:0x149ba794fc1de8f6c05d6b209fa655ef1666a057',    # https://zora.co/collect/zora:0x149ba794fc1de8f6c05d6b209fa655ef1666a057   - Rainbow is for everyone от Rainbow Wallet
                  'https://zora.co/collect/zora:0x86477e3b43a2f7dd2f2b3480ddbc2555f4edb074',    # https://zora.co/collect/zora:0x86477e3b43a2f7dd2f2b3480ddbc2555f4edb074   - Introducing: Rainbow Extension от Rainbow Wallet 
                  'https://zora.co/collect/base:0x1fa2faf72b78ab9e6a1424f31252dbef459638f4']    # https://zora.co/collect/base:0x1fa2faf72b78ab9e6a1424f31252dbef459638f4   - Double Rainbow (BASE) от Rainbow Wallet
                                                                                                # Минт любых других NFT на Zora.co (Будет рандомная из списка)
                                                                                                # Сюда пишем url NFT
QUANTITY_NFT_8 = [1, 1]                            # Количество NFT для минта
NUMBER_TRANS_8 = [1, 1]                            # Количество транзакций             [min, max]

# 15 - Mint NFTS2ME || FREE MINT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_15 = [10, 20]                         # Количество NFT для минта
NUMBER_TRANS_15 = [2, 3]                           # Количество транзакций             [min, max]

# 16 - Mint.fun || FREE MINT ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Количество нфт выберается автоматически для бесплатного минта

NUMBER_TRANS_16 = [2, 3]                           # Количество транзакций             [min, max]

# 19 - Send money yourself -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NUMBER_TRANS_YOURSELF = [1, 2]                     # Количеcтво транзакций самому себе [min, max]

# 21 - Custom routes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

routes = ['mint_zorb_zora', 'create_contract', 'update_nft_metadata', 'send_money_yourself', 'mint_bridge_nft', 'mintfun', 'mint_opensea_zorb_zora', 'mint_nft2me']

routes_shuffle        = True                       # Перемешивает модули || True/ False
time_delay_routes_min = 100                        # Минимальная и
time_delay_routes_max = 200                        # Максимальная задержка между модулями

#           Список доступных модулей
#           'merkly_refuel',                        - Merkly refuel
#           'zerius_refuel',                        - Zerius refuel
#           'mint_bridge_nft_zerius'                - Mint NFT Zerius + bridge
#           'mint_bridge_nft_l2pass'                - Mint NFT L2PASS + bridge
#           'mint_zorb_zora'                        - Mint PYTHON ZORB в сети ZORA     (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_base'                        - Mint PYTHON ZORB в сети BASE     (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_optimism'                    - Mint PYTHON ZORB в сети OPTIMISM (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_opensea_zorb_zora'                - Mint PYTHON ZORB через OpenSea в сети ZORA     (FREE MINT)
#           'mint_opensea_zorb_base'                - Mint PYTHON ZORB через OpenSea в сети BASE     (FREE MINT)
#           'mint_opensea_zorb_optimism'            - Mint PYTHON ZORB через OpenSea в сети OPTIMISM (FREE MINT)
#           'mint_nft2me'                           - Mint NFTS2ME (FREE MINT)
#           'create_contract'                       - Create contract NFT ERC1155 (Zora.co)
#           'mint_custom_nft',                      - Mint Custom NFT
#           'update_nft_metadata',                  - Update NFT metadata
#           'send_money_yourself',                  - Send money yourself
#           'mintfun'                               - Mint free NFT from Mint.fun
