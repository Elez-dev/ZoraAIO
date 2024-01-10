from web3.exceptions import TransactionNotFound
from loguru import logger
from settings import RETRY
import time


def exception_handler(func):
    def wrapper(self, *args, **kwargs):
        for _ in range(RETRY):
            try:
                return func(self, *args, **kwargs)

            except TransactionNotFound:
                logger.error('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз\n')
                time.sleep(30)

            except ConnectionError:
                logger.error('Ошибка подключения к интернету или проблемы с РПЦ\n')
                time.sleep(30)

            except Exception as error:
                if isinstance(error.args[0], dict):
                    if 'insufficien' in error.args[0]['message']:
                        logger.error('Ошибка, скорее всего нехватает комсы\n')
                        return 'balance'
                    else:
                        logger.error(error)
                        time.sleep(30)
                else:
                    logger.error(error)
                    time.sleep(30)
        else:
            return False
    return wrapper
