import requests
from datetime import datetime
from utils.wallet import Wallet
import ua_generator
import uuid
import time
import random
from eth_account.messages import encode_defunct
from loguru import logger
import imaplib
import email
from email.header import decode_header
from settings import IMAP_SERVER
from utils.func import sleeping
import re
from utils.retry import exception_handler


class SetEmail(Wallet):
    def __init__(self, private_key, number, proxy):
        super().__init__(private_key, 'Zora', number, proxy)
        self.privy_ca_id = str(uuid.uuid4())
        self.session = requests.Session()
        if self.proxy is not None:
            proxy_dick = {'https': 'http://' + self.proxy, 'http': 'http://' + self.proxy}
            self.session.proxies = proxy_dick

    def get_call_data_get(self, url, json=None):
        if json is None:
            resp = self.session.get(url=url)
        else:
            resp = self.session.get(url=url, json=json)
        if resp.status_code >= 400:
            return False
        return resp.json()

    def get_call_data_post(self, url, json):
        resp = self.session.post(url=url, json=json)
        return resp.json()

    def generate_headers(self):
        ua = ua_generator.generate(device='desktop', browser='chrome')
        headers = {
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://zora.co',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'referer': 'https://zora.co/',
            'privy-app-id': 'clpgf04wn04hnkw0fv1m11mnb',
            'privy-ca-id': self.privy_ca_id,
            'privy-client': 'react-auth:1.51.1',
            'sec-ch-ua': f'"{ua.ch.brands[2:]}"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': f'"{ua.platform.title()}"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': ua.text
        }
        self.session.headers = headers

    def get_nonce(self):
        url = 'https://auth.privy.io/api/v1/siwe/init'
        json = {'address': self.address_wallet}
        data = self.get_call_data_post(url=url, json=json)
        return data['nonce']

    def sign_in(self):
        self.generate_headers()
        nonce = self.get_nonce()
        issued_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        time.sleep(random.uniform(0.5, 1.5))

        msg = f'zora.co wants you to sign in with your Ethereum account:\n' \
              f'{self.address_wallet}\n\n' \
              f'By signing, you are proving you own this wallet and logging in. ' \
              f'This does not initiate a transaction or cost any fees.\n\n' \
              f'URI: https://zora.co\n' \
              f'Version: 1\n' \
              f'Chain ID: 1\n' \
              f'Nonce: {nonce}\n' \
              f'Issued At: {issued_at}\n' \
              f'Resources:\n' \
              f'- https://privy.io'
        message = encode_defunct(text=msg)
        signature = self.account.sign_message(message).signature.hex()
        url = 'https://auth.privy.io/api/v1/siwe/authenticate'
        json = {
            'chainId': 'eip155:7777777',
            'connectorType': 'injected',
            'message': msg,
            'signature': signature,
            'walletClientType': 'metamask',
        }
        res = self.session.post(url=url, json=json)
        data = res.json()
        head = res.headers['Set-Cookie']
        privy_refresh_token = re.search(r'privy-refresh-token=([^;,]+)', head).group(1)
        privy_access_token = re.search(r'privy-access-token=([^;,]+)', head).group(1)
        token = data['token']
        self.session.cookies.update({
            'device_id': str(uuid.uuid4()),
            'zora-news-announcement-1': '2023-11-20T16:42:27Z',
            'wallet_address': self.address_wallet,
            'privy-token': token,
            'privy-refresh-token': privy_refresh_token,
            'privy-access-token': privy_access_token,
            'privy-session': 't'
        })
        self.session.headers.update({'Authorization': 'Bearer ' + token})
        logger.success('Signed in')

    @exception_handler('Get email info')
    def get_existed_email(self):
        self.sign_in()
        url = 'https://zora.co/api/account'
        data = self.get_call_data_get(url)
        if data is False:
            return False
        if 'account' not in data:
            return False
        if data['account']['emailVerified'] is False:
            return False
        return True

    @exception_handler('Setting new email')
    def set_email(self, email_info):
        email_username = email_info.split(':')[0]
        logger.info(f'Setting new email')
        url = 'https://privy.zora.co/api/v1/passwordless/init'
        json = {'email': email_username}
        data = self.get_call_data_post(url, json)
        if data['success'] is True:
            logger.info('Sent the code by email')

    @exception_handler('Veridy email')
    def verify_email(self, email_info):
        email_username, email_password = email_info.split(':')
        imap = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap.login(email_username, email_password)
        status, folders = imap.list()
        for folder in folders:
            folder_name = folder.decode('utf-8').split(' "/" ')[1]
            if self.check_folder(email_username, imap, folder_name):
                return True

    def check_folder(self, email_username, imap, folder):
        messages = imap.select(folder)[1]
        msg_cnt = int(messages[0])
        for i in range(msg_cnt, 0, -1):
            res, msg = imap.fetch(str(i), '(RFC822)')
            raw_email = msg[0][1]
            msg = email.message_from_bytes(raw_email)
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)

            if ' is your login code for Zora' not in subject or len(subject) != 34:
                continue

            code = subject.split(' ')[0]
            url = 'https://privy.zora.co/api/v1/passwordless/link'
            json = {
                'code': code,
                'email': email_username,
            }
            self.get_call_data_post(url, json)
            logger.success('Mail successfully linked\n')
            return True
        return False

    def link_email(self, mail):
        res = self.get_existed_email()
        if res is False:
            self.set_email(mail)
            sleeping(50, 100)
            self.verify_email(mail)
