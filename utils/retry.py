from web3.exceptions import TransactionNotFound
from loguru import logger
from settings import RETRY, TIME_DELAY_ERROR, TG_BOT_SEND, REFUEL
from utils.tg_bot import TgBot
from utils.func import sleeping
from utils.refuel import Refuel


def exception_handler(label=''):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            for _ in range(RETRY):
                try:
                    return func(self, *args, **kwargs)

                except TransactionNotFound:
                    logger.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз\n')
                    if TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, label, self.address_wallet,
                                                 'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
                    sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

                except ConnectionError:
                    logger.error('Ошибка подключения к интернету или проблемы с РПЦ\n')
                    if TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, label, self.address_wallet,
                                                 'Ошибка подключения к интернету или проблемы с РПЦ')
                    sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

                except Exception as error:
                    if isinstance(error.args[0], dict):
                        if 'insufficien' in error.args[0]['message'] or 'required exceeds allowance' in error.args[0]['message']:
                            logger.error('Ошибка, скорее всего нехватает комсы\n')
                            if TG_BOT_SEND is True:
                                TgBot.send_message_error(self, self.number, label, self.address_wallet,
                                                         'Ошибка, скорее всего нехватает комсы')

                            if REFUEL is True:
                                tun = Refuel(self.private_key, self.chain, self.number, self.proxy)
                                res = tun.refuel()
                                if res == 'error':
                                    return 'balance'
                                sleeping(100, 200)
                                continue

                            return 'balance'
                        else:
                            logger.error(error)
                            if TG_BOT_SEND is True:
                                TgBot.send_message_error(self, self.number, label, self.address_wallet, error)
                            sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])
                    else:
                        logger.error(error)
                        if TG_BOT_SEND is True:
                            TgBot.send_message_error(self, self.number, label, self.address_wallet, error)
                        sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])
            else:
                return False
        return wrapper
    return decorator
