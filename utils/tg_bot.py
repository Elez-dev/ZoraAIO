from settings import TG_ID, TG_TOKEN
import requests
import json


class TgBot:

    @staticmethod
    def send_message(text):
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        params = {
            'chat_id': TG_ID,
            'text': text,
            'link_preview_options': json.dumps({'is_disabled': True}),
            'parse_mode': 'HTML'
        }
        requests.get(url=url, data=params)

    def send_message_success(self, number, text, address, link):
        try:
            str_send = f'[{number}]\n✅ {text}\nАккаунт: <a href="https://debank.com/profile/{address}">{address}</a>\n<a href="{link}">Tx hash</a>'

            self.send_message(str_send)
        except Exception as error:
            print(error)

    def send_message_error(self, number, text, address, errorr):
        try:
            str_send = f'[{number}]\n❌ {text}\nАккаунт: <a href="https://debank.com/profile/{address}" >{address}</a >\n{errorr}'
            self.send_message(str_send)
        except Exception as error:
            print(error)
