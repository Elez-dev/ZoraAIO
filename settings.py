from utils.chain import *

EXCEL_PASSWORD  = False                             # Если ставите пароль на Excel с приватниками || True/ False
SHUFFLE_WALLETS = True                              # Перемешка кошельков                         || True/ False

TG_BOT_SEND = False                                 # Включить уведомления в тг или нет           || True/ False
TG_TOKEN = ''                                       # API токен тг-бота - создать его можно здесь - https://t.me/BotFather
TG_ID = 0000                                        # id твоего телеграмма можно узнать тут       - https://t.me/getmyid_bot

CHAIN_RPC = {
    Arbitrum: 'https://1rpc.io/arb',
    Optimism: 'https://1rpc.io/op',
    Polygon : 'https://1rpc.io/matic',
    Zora    : 'https://rpc.zora.energy',            # https://zora.rpc.thirdweb.com | https://rpc.zora.energy | https://rpc.zerion.io/v1/zora
    Ethereum: 'https://rpc.ankr.com/eth',
    Base    : 'https://rpc.ankr.com/base',
    Nova    : 'https://rpc.ankr.com/arbitrumnova',
    zkSync  : 'https://rpc.ankr.com/zksync_era',
    Linea   : 'https://1rpc.io/linea',
    Blast   : 'https://rpc.ankr.com/blast'
}

MAX_GAS_ETH = 50                                    # gas в gwei (смотреть здесь : https://etherscan.io/gastracker)
ZORA_GASPRICE_PRESCALE = 0.001                      # Использовать Max base fee и Priority fee для газа в Zora, экономия 0.3-0.5$
BLAST_GASPRICE_PRESCALE = 0.001                     # Использовать Max base fee и Priority fee для газа в Blast

RETRY = 3                                           # Количество попыток при ошибках / фейлах

TIME_DELAY = [50, 70]                               # Задержка после ТРАНЗАКЦИЙ     [min, max]
TIME_ACCOUNT_DELAY = [50, 75]                       # Задержка между АККАУНТАМИ     [min, max]
TIME_DELAY_ERROR = [10, 20]                         # Задержка при ошибках / фейлах [min, max]

MOBILE_PROXY = False                                # Если юзаете мобильные прокси -> True, если обычные или VPN -> False
MOBILE_DATA = 'login:pass@ip:port'                  # Сюда пишем проксю в формате login:pass@ip:port
MOBILE_CHANGE_IP_LINK = ''                          # Сюда пишем ссылку для смены IP

# 1 - Официальный мост https://bridge.zora.energy  -----------------------------------------------------------------------------------------------------------------------------------------------

OFF_ZORA_DEPOSIT = [0.005, 0.01, 5]                 # Сумма для депозита [min, max, round_decimal]
                                                    # Если сумма больше чем на балансе, будет бридж всего баланса

# 2 - INSTANT BRIDGE https://relay.link  ------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Nova, Base, Zora, ZkSync, Linea, Blast

CHAIN_FROM_TUNNEL = Optimism                        # Из какой сети
CHAIN_TO_TUNNEL   = Zora                            # В какую сеть
VALUE_TUNNEL      = [0.0001, 0.0002, 4]             # Количество [min, max, round_decimal]

# 3 - Merkly ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_MERKLY = Optimism                        # Из какой сети
CHAIN_TO_MERKLY   = Zora                            # В какую сеть
VALUE_MERKLY      = [0.0015, 0.0035, 4]             # Количество [min, max, round_decimal]


# 9 - 10 Wrap unwrap ETH -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PRESCALE = [0.01, 0.02, 3]                          # [min, max, round_decimal]
NUMBER_TRANS_9 = [1, 1]                             # Количество транзакций             [min, max]

# 11 Uniswap ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


VALUE_SWAP = [0.00001, 0.00002, 5]                             # [min, max, decimal]
TOKEN_SWAP = ['0xa6b280b42cb0b7c4a4f789ec6ccc3a7609a1bc39']  # Сюда вписывать контракты токенов для свапа
                                                             # Будет выбираться рандомно из списка
                                                             # 0x078540eECC8b6d89949c9C7d5e8E91eAb64f6696 - $IMAGINE
                                                             # 0xa6b280b42cb0b7c4a4f789ec6ccc3a7609a1bc39 - $ENJOY
NUMBER_TRANS_11 = [1, 1]                                     # Количество транзакций    [min, max]

# 12 - 16 || Mint PYTHON ZORB (Zora.co) --------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_6 = [1, 1]                             # Количество NFT для минта
NUMBER_TRANS_6 = [1, 1]                             # Количество транзакций             [min, max]

# 17 - 19 || Mint PYTHON ZORB (OpenSea) || FREE MINT -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_7 = [1, 70]                            # Количество NFT для минта
NUMBER_TRANS_7 = [1, 1]                             # Количество транзакций             [min, max]

# 20 - Mint Custom NFT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

URL_CUSTOM_NFT = ['https://zora.co/collect/zora:0xc7d47ae78fc27520633aa7c27b23758b4c429e30/1']   # Минт любых других NFT на Zora.co (Будет рандомная из списка)   Сюда пишем url NFT
    
QUANTITY_NFT_8 = [1, 1]                             # Количество NFT для минта
NUMBER_TRANS_8 = [1, 1]                             # Количество транзакций             [min, max]

# 21 - Mint NFTS2ME || FREE MINT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_15 = [1, 20]                           # Количество NFT для минта
NUMBER_TRANS_15 = [1, 3]                            # Количество транзакций             [min, max]

# 22 - Mint.fun || FREE MINT ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Количество нфт выберается автоматически для бесплатного минта

NUMBER_TRANS_16 = [2, 3]                            # Количество транзакций             [min, max]

# 26 - Send money yourself -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NUMBER_TRANS_YOURSELF = [1, 1]                      # Количеcтво транзакций самому себе [min, max]

# Module 27 - IMAP сервер для почт

IMAP_SERVER = 'imap.rambler.ru'

# 30 - Custom routes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

routes = [
    ['mint_zorb_zora', 'mintfun', 'mint_opensea_zorb_zora'],
    ['mint_opensea_zorb_optimism', 'mint_opensea_zorb_base', None],
    ['mint_opensea_zorb_zora', 'mint_opensea_zorb_zora', 'mintfun'],
    ['mint_custom_nft', 'mint_zorb_zora', None],
    ['wrap_unwrap', 'mint_zorb_base', 'send_money_yourself'],
    ['mint_opensea_zorb_optimism', 'mint_opensea_zorb_base', None],
    ['buy_token']
]

routes_shuffle = True                                # Перемешивает модули || True/ False
TIME_DELAY_ROUTES = [100, 120]                       # [min, max] Задержка между модулями


#           Список доступных модулей
#           'mint_zorb_zora'                        - Mint PYTHON ZORB в сети ZORA        (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_base'                        - Mint PYTHON ZORB в сети BASE        (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_optimism'                    - Mint PYTHON ZORB в сети OPTIMISM    (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_arbitrum'                    - Mint THE AMBASSADOR в сети Arbitrum (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_opensea_zorb_zora'                - Mint PYTHON ZORB через OpenSea в сети ZORA     (FREE MINT)
#           'mint_opensea_zorb_base'                - Mint PYTHON ZORB через OpenSea в сети BASE     (FREE MINT)
#           'mint_opensea_zorb_optimism'            - Mint PYTHON ZORB через OpenSea в сети OPTIMISM (FREE MINT)
#           'mint_nft2me'                           - Mint NFTS2ME (FREE MINT)
#           'create_contract'                       - Create contract NFT ERC1155 (Zora.co)
#           'mint_custom_nft',                      - Mint Custom NFT
#           'update_nft_metadata',                  - Update NFT metadata
#           'send_money_yourself',                  - Send money yourself
#           'mintfun'                               - Mint free NFT from Mint.fun
#           'wrap_unwrap'                           - Wrap + Unwrap ETH
#           'swap'                                  - Покупка + продажа на Uniswap
#           'buy_token'                             - Покупка выбранного токена на Uniswap
#           'mint_for_enjoy'                        - Минт NFT за $ENJOY
#           'mint_for_imagine'                      - Минт NFT за $IMAGINE

# Refuel -----------------------------------------------------------------------------------------------------------------------

REFUEL = False  # Если баланса в Zora будет недостаточно будет сделан Refuel с помощью INSTANT bridge (Если False то делаться не будет)

# Из каких сетей делать refuel (Будет выбрана та, где больший баланс)
# Доступно: Arbitrum, Optimism, Polygon, Base, Nova, zkSync, Linea

CHAIN_FROM_REFUEL = [Arbitrum, Optimism, Polygon, Base, Nova, zkSync, Linea]

VALUE_REFUEL = {
    Polygon: [1.01, 1.5, 3],                      # [min, max, round_decimal]
    'Other': [0.00001, 0.0001, 6]                 # [min, max, round_decimal] Здесь сумма относится ко всем остальным сетям, т.к. для оплаты используется ETH
}

# 31 Mint NFT for $ENJOY -------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_31 = [1, 1]                          # Количество NFT для минта          [min, max]
NUMBER_TRANS_31 = [1, 3]                          # Количество транзакций             [min, max]

# 32 Mint NFT for $IMAGINE ---------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_32 = [1, 1]                          # Количество NFT для минта          [min, max]
NUMBER_TRANS_32 = [1, 3]                          # Количество транзакций             [min, max]
