import io
from msoffcrypto.exceptions import DecryptionError, InvalidKeyError
from loguru import logger
from settings import EXCEL_PASSWORD, SHUFFLE_WALLETS
import random
from tqdm import tqdm
import time
import msoffcrypto
import pandas as pd


def shuffle(wallets_list):
    if SHUFFLE_WALLETS is True:
        numbered_wallets = list(enumerate(wallets_list, start=1))
        random.shuffle(numbered_wallets)
    elif SHUFFLE_WALLETS is False:
        numbered_wallets = list(enumerate(wallets_list, start=1))
    else:
        raise ValueError("\nНеверное значение переменной 'shuffle_wallets'. Ожидается 'True' or 'False'.")
    return numbered_wallets


def sleeping(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    time.sleep(1)
    with tqdm(
            total=delay,
            desc="💤 Sleep",
            bar_format="{desc}: |{bar:20}| {percentage:.0f}% | {n_fmt}/{total_fmt}",
            colour="green"
    ) as pbar:
        for _ in range(delay):
            time.sleep(1)
            pbar.update(1)
    time.sleep(1)
    print()


def get_accounts_data():
    decrypted_data = io.BytesIO()
    with open('./data/accounts_data.xlsx', 'rb') as file:
        if EXCEL_PASSWORD:
            time.sleep(1)
            password = input('Enter the password: ')
            office_file = msoffcrypto.OfficeFile(file)

            try:
                office_file.load_key(password=password)
            except msoffcrypto.exceptions.DecryptionError:
                logger.info('\n⚠️ Incorrect password to decrypt Excel file! ⚠️\n')
                raise DecryptionError('Incorrect password')

            try:
                office_file.decrypt(decrypted_data)
            except msoffcrypto.exceptions.InvalidKeyError:
                logger.info('\n⚠️ Incorrect password to decrypt Excel file! ⚠️\n')
                raise InvalidKeyError('Incorrect password')

            except msoffcrypto.exceptions.DecryptionError:
                logger.info('\n⚠️ Set password on your Excel file first! ⚠️\n')
                raise DecryptionError('Excel without password')

            office_file.decrypt(decrypted_data)

            try:
                wb = pd.read_excel(decrypted_data)
            except ValueError as error:
                logger.info('\n⚠️ Wrong page name! ⚠️\n')
                raise ValueError(f"{error}")
        else:
            try:
                wb = pd.read_excel(file)
            except ValueError as error:
                logger.info('\n⚠️ Wrong page name! ⚠️\n')
                raise ValueError(f"{error}")

        accounts_data = {}
        for index, row in wb.iterrows():
            private_key_evm = row["Private Key EVM"]
            proxy = row['PROXY']
            nft = row['ADDRESS NFT TO UPDATE METADATA']
            accounts_data[int(index) + 1] = {
                "private_key_evm": private_key_evm,
                "proxy": proxy,
                'nft': nft
            }

        priv_key_evm, prx, nftt = [], [], []
        for k, v in accounts_data.items():
            priv_key_evm.append(v['private_key_evm'])
            prx.append(v['proxy'] if isinstance(v['proxy'], str) else None)
            nftt.append(v['nft'] if isinstance(v['nft'], str) else None)

        return combine_lists(priv_key_evm, prx, nftt)


def combine_lists(list1, list2, list3):
    combined_list = []
    length = len(list1)

    for i in range(length):
        combined_list.append((list1[i], list2[i], list3[i]))

    return combined_list
