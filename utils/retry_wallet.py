from web3.exceptions import TransactionNotFound
from settings import RETRY, TIME_DELAY_ERROR
from loguru import logger
from utils.func import sleeping


def exception_handler_wallet(func):
    def wrapper(self, *args, **kwargs):
        for _ in range(RETRY):

            try:
                return func(self, *args, **kwargs)

            except TransactionNotFound:
                logger.info('Транзакция не смайнилась за долгий промежуток времени, пытаюсь еще раз')
                sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

            except ConnectionError:
                logger.info('Ошибка подключения к интернету или проблемы с РПЦ')
                sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])

            except Exception as error:
                logger.info('Произошла ошибка')

                if isinstance(error.args[0], str):

                    if 'is not in the chain after' in error.args[0]:
                        logger.error('Транзакция не смайнилась за долгий промежуток времени. Пытаюсь еще раз')

                    elif error.args[0] == "balance refuel":
                        logger.error('Need refuel\n')

                    else:
                        logger.error(error)

                elif isinstance(error.args[0], dict):
                    if 'nsufficien' in error.args[0]['message'] or 'required exceeds allowance' in error.args[0]['message']:
                        logger.error('Need refuel\n')

                    elif 'execute this request' in error.args[0]['message']:
                        logger.error('Ошибка запроса на RPC, пытаюсь еще раз')

                    elif 'ax fee per gas' in error.args[0]['message']:
                        logger.error('Ошибка газа, пытаюсь еще раз')

                    else:
                        logger.error(f'{error}\n')

                else:
                    logger.error(f'{error}\n')
                sleeping(TIME_DELAY_ERROR[0], TIME_DELAY_ERROR[1])
        else:
            raise ValueError('the number of iterations of the loop has ended')
    return wrapper
