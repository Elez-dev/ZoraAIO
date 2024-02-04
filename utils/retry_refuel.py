from web3.exceptions import TransactionNotFound
from loguru import logger
from settings import RETRY, TIME_DELAY_ERROR
from settings import TG_BOT_SEND
from utils.tg_bot import TgBot
from utils.func import sleeping


def exception_handler_refuel(func):
    def wrapper(self, *args, **kwargs):
        for _ in range(RETRY):

            try:
                return func(self, *args, **kwargs)

            except TransactionNotFound:
                logger.info('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
                if TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'Refuel', self.address_wallet,
                                             'Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
                sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

            except ConnectionError:
                logger.info('Ошибка подключения к интернету или проблемы с РПЦ')
                if TG_BOT_SEND is True:
                    TgBot.send_message_error(self, self.number, 'Refuel', self.address_wallet,
                                             'Ошибка подключения к интернету или проблемы с РПЦ')
                sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

            except Exception as error:
                logger.info('Произошла ошибка')
                if isinstance(error.args[0], dict):
                    if 'insufficien' in error.args[0]['message']:
                        logger.error('Ошибка, скорее всего нехватает комсы\n')
                        if TG_BOT_SEND is True:
                            TgBot.send_message_error(self, self.number, 'Refuel', self.address_wallet,
                                                     'Ошибка, скорее всего нехватает комсы')
                        return 'balance'
                    else:
                        logger.error(error)
                        if TG_BOT_SEND is True:
                            TgBot.send_message_error(self, self.number, 'Refuel', self.address_wallet, error)
                        sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])
                else:
                    logger.error(error)
                    if TG_BOT_SEND is True:
                        TgBot.send_message_error(self, self.number, 'Refuel', self.address_wallet, error)
                    sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

                sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])
        else:
            raise ValueError('the number of iterations of the loop has ended')
    return wrapper