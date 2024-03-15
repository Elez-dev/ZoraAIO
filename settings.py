from utils.chain import *

EXCEL_PASSWORD  = False                             # Если ставите пароль на Excel с приватниками || True/ False
SHUFFLE_WALLETS = True                              # Перемешка кошельков                         || True/ False

TG_BOT_SEND = False                                 # Включить уведомления в тг или нет           || True/ False
TG_TOKEN = ''                                       # API токен тг-бота - создать его можно здесь - https://t.me/BotFather
TG_ID = 0                                           # id твоего телеграмма можно узнать тут       - https://t.me/getmyid_bot

CHAIN_RPC = {
    Arbitrum: 'https://1rpc.io/arb',
    Optimism: 'https://1rpc.io/op',
    Polygon : 'https://1rpc.io/matic',
    Zora    : 'https://zora.rpc.thirdweb.com',      # https://zora.rpc.thirdweb.com | https://rpc.zora.energy | https://rpc.zerion.io/v1/zora
    Ethereum: 'https://rpc.ankr.com/eth',
    Base    : 'https://rpc.ankr.com/base',
    Nova    : 'https://rpc.ankr.com/arbitrumnova',
    zkSync  : 'https://rpc.ankr.com/zksync_era',
    Linea   : 'https://1rpc.io/linea',
    Blast   : 'https://rpc.ankr.com/blast'
}

MAX_GAS_ETH = 50                                    # gas в gwei (смотреть здесь : https://etherscan.io/gastracker)
ZORA_GASPRICE_PRESCALE = 0.001                      # Использовать Max base fee и Priority fee для газа в Zora, экономия 0.3-0.5$
BASE_GASPRICE_PRESCALE = 0.001                      # Использовать Max base fee и Priority fee для газа в Base
BLAST_GASPRICE_PRESCALE = 0.001                     # Использовать Max base fee и Priority fee для газа в Blast

RETRY = 3                                           # Количество попыток при ошибках / фейлах
TIME_DELAY = [100, 200]                             # Задержка после ТРАНЗАКЦИЙ     [min, max]
TIME_ACCOUNT_DELAY = [100, 150]                     # Задержка между АККАУНТАМИ     [min, max]
TIME_DELAY_ERROR = [10, 20]                         # Задержка при ошибках / фейлах [min, max]

MOBILE_PROXY = False                                # Если юзаете мобильные прокси -> True, если обычные или VPN -> False
MOBILE_DATA = 'login:pass@ip:port'                  # Сюда пишем проксю в формате login:pass@ip:port
MOBILE_CHANGE_IP_LINK = ''                          # Сюда пишем ссылку для смены IP

# 1 - Официальный мост https://bridge.zora.energy  -----------------------------------------------------------------------------------------------------------------------------------------------

OFF_ZORA_DEPOSIT = [0.005, 0.01, 5]                    # Сумма для депозита [min, max, round_decimal]
                                                    # Если сумма больше чем на балансе, будет бридж всего баланса

# 2 - Relay.link bridge https://relay.link  ------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Nova, Base, Zora, ZkSync, Linea, Blast
# UPD!!! Проверяйте на сайте (https://relay.link/) список доступных сетей. Иногда какие-то могут отключать
# Максимальная сумма бриджа - 0.5 ETH

CHAIN_FROM_TUNNEL = Optimism                        # Из какой сети
CHAIN_TO_TUNNEL   = Zora                            # В какую сеть
VALUE_TUNNEL      = [0.0001, 0.0002, 4]             # Количество [min, max, round_decimal]

# 3 - Merkly ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_MERKLY = Optimism                        # Из какой сети
CHAIN_TO_MERKLY   = Zora                            # В какую сеть
VALUE_MERKLY      = [0.0015, 0.0035, 4]             # Количество [min, max, round_decimal]

# 4 - 6 || Zerius -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Список доступных сетей: Arbitrum, Optimism, Polygon, Base, Zora

CHAIN_FROM_ZERIUS = Optimism                        # Из какой сети
CHAIN_TO_ZERIUS   = Zora                            # В какую сеть
VALUE_ZERIUS = [0.002, 0.004, 4]                    # Количество [min, max, round_decimal]

CHAIN_TO_BRIDGE_ZERIUS = Base                       # В какую сеть бридж NFT

# 7 - 8 || L2PASS -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

CHAIN_TO_BRIDGE_L2 = Base                           # В какую сеть бридж NFT

# 9 - 10 Wrap unwrap ETH -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PRESCALE = [0.01, 0.02, 3]                            # [min, max, round_decimal]
NUMBER_TRANS_9 = [1, 1]                             # Количество транзакций             [min, max]

# 11 Uniswap ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

VALUE_SWAP = [0.0000001, 0.000001, 7]                        # [min, max, decimal] СВАПАТЬ ТОЛЬКО НА МАЛЕНЬКИЕ СУММЫ !!!
TOKEN_SWAP = ['0x0416c274A5b50B23cb311c9fdc7659490417d1B7',  # Сюда вписывать контракты токенов для свапа
              '0x0416c274A5b50B23cb311c9fdc7659490417d1B7'
              ]                                              # Будет выбираться рандомно из списка

NUMBER_TRANS_11 = [1, 1]                                     # Количество транзакций    [min, max]

# 12 - 16 || Mint PYTHON ZORB (Zora.co) --------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_6 = [1, 1]                             # Количество NFT для минта
NUMBER_TRANS_6 = [1, 1]                             # Количество транзакций             [min, max]

# 17 - 19 || Mint PYTHON ZORB (OpenSea) || FREE MINT -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_7 = [100, 700]                         # Количество NFT для минта
NUMBER_TRANS_7 = [1, 1]                             # Количество транзакций             [min, max]

# 20 - Mint Custom NFT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

URL_CUSTOM_NFT = ['https://zora.co/collect/zora:0x0de78cc261622a04784a642eaf9008870e169588/1',
                  'https://zora.co/collect/zora:0x651c54886153c96df8e0764abce9d13416c841f8/1']  # Минт любых других NFT на Zora.co (Будет рандомная из списка)
                                                                                                # Сюда пишем url NFT
    
QUANTITY_NFT_8 = [1, 1]                             # Количество NFT для минта
NUMBER_TRANS_8 = [1, 1]                             # Количество транзакций             [min, max]

# 21 - Mint NFTS2ME || FREE MINT -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

QUANTITY_NFT_15 = [10, 20]                          # Количество NFT для минта
NUMBER_TRANS_15 = [1, 3]                            # Количество транзакций             [min, max]

# 22 - Mint.fun || FREE MINT ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Количество нфт выберается автоматически для бесплатного минта

NUMBER_TRANS_16 = [2, 3]                            # Количество транзакций             [min, max]

# 26 - Send money yourself -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

NUMBER_TRANS_YOURSELF = [1, 2]                      # Количеcтво транзакций самому себе [min, max]

# Module 27 - IMAP сервер для почт

IMAP_SERVER = 'imap.rambler.ru'

# 30 - Custom routes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

routes = [
    ['mint_zorb_zora'],
    ['create_contract', None],
    ['mint_zorb_base'],
    ['mint_nft2me'],
    ['mint_zorb_arbitrum'],
    ['mintfun'],
    ['mint_nft2me', None],                          # Если будет выбран None, то данный модуль ['mint_nft2me', None] будет пропущен 
    ['mint_opensea_zorb_zora']
]

routes_shuffle = True                                # Перемешивает модули || True/ False
TIME_DELAY_ROUTES = [100, 120]                       # [min, max] Задержка между модулями

#           Список доступных модулей
#           'merkly_refuel',                        - Merkly refuel
#           'zerius_refuel',                        - Zerius refuel
#           'mint_bridge_nft_zerius'                - Mint NFT Zerius + bridge
#           'mint_bridge_nft_l2pass'                - Mint NFT L2PASS + bridge
#           'mint_zorb_zora'                        - Mint PYTHON ZORB в сети ZORA        (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_base'                        - Mint PYTHON ZORB в сети BASE        (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_optimism'                    - Mint PYTHON ZORB в сети OPTIMISM    (С официальной комиссией ZORA 0.000777 ETH)
#           'mint_zorb_blast'                       - Mint PYTHON ZORB в сети Blast       (С официальной комиссией ZORA 0.000777 ETH)
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

# Refuel -----------------------------------------------------------------------------------------------------------------------

REFUEL = False  # Если баланса в Zora будет недостаточно будет сделан Refuel с помощью Tunnel bridge (Если False то делаться не будет)

# Из каких сетей делать refuel (Будет выбрана та, где больший баланс)
# Доступно: Arbitrum, Optimism, Polygon, Base, Nova, zkSync, Linea

CHAIN_FROM_REFUEL = [Arbitrum, Optimism, Polygon, Base, Nova, zkSync, Linea]

VALUE_REFUEL = {
    Polygon: [1.01, 1.5, 3],       # [min, max, round_decimal]
    'Other': [0.00001, 0.0001, 6]  # [min, max, round_decimal] Здесь сумма относится ко всем остальным сетям, т.к. для оплаты используется ETH
}

