import json
import hmac
import hashlib
import requests
import urllib
import time
from urllib.parse import urlparse
from config import Tokens


# Возвращает цену пары в USD или 0
def get_pair_price(ticker='BTC'):
    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={ticker}USDT')
    if 'Invalid symbol' in response.text:
        return 0
    else:
        pair_price = json.loads(response.text)
        return pair_price['price']


class Binance:
    """Обертка для Binance API"""
    def __init__(self, api_key, api_secret):
        self.base_url = 'https://api.binance.com/'
        self.API_KEY = api_key
        self.API_SECRET = bytearray(api_secret, encoding='utf-8')

    def call_api(self, url):
        """Генерируем подпись"""
        payload = {'timestamp': int(time.time() - 1) * 1000}
        payload_str = urllib.parse.urlencode(payload).encode('utf-8')
        sign = hmac.new(key=self.API_SECRET, msg=payload_str, digestmod=hashlib.sha256).hexdigest()
        payload_str = payload_str.decode("utf-8") + "&signature=" + str(sign)

        response = requests.request(method='GET', url=self.base_url + url + '?' + payload_str,
                                    headers={"X-MBX-APIKEY": self.API_KEY,
                                             "Content-Type": "application/x-www-form-urlencoded"})
        obj = json.loads(response.text)
        return obj

    def get_wallet(self):
        """Возвращаем спотовый кошелек"""
        coins = self.call_api('api/v3/account')
        wallet = []
        balance_total = 0.00
        for coin in coins['balances']:
            ticker = coin['asset']
            amount = float(coin['free'])
            if amount == 0:
                continue
            price_in_usd = float(get_pair_price(ticker))
            balance = amount * price_in_usd
            wallet.append([ticker, amount, price_in_usd, balance])
            balance_total += balance
        wallet.append(balance_total)
        return wallet

    def get_deposits(self):
        """Возвращаем депозиты"""
        coins = self.call_api('/sapi/v1/lending/daily/token/position')
        deposits = []
        balance_total = 0.00
        for coin in coins:
            ticker = coin['asset']
            amount_freeze = float(coin['totalAmount'])
            earn = float(coin['totalInterest'])
            amount_total = amount_freeze + earn
            price_in_usd = float(get_pair_price(ticker))
            balance = amount_total * price_in_usd
            profit = earn * price_in_usd
            deposits.append([ticker, amount_freeze, earn, amount_total, price_in_usd, balance, profit])
            balance_total += balance
        deposits.append(balance_total)
        return deposits


def build_collection_crypto():
    """Собираем коллекцию для передачи в шаблон"""
    bn = Binance(Tokens.BINANCE_API_KEY, Tokens.BINANCE_API_SECRET)
    wallet = bn.get_wallet()
    balance_wallet = wallet.pop(-1)
    deposits = bn.get_deposits()
    balance_deposits = deposits.pop(-1)
    return wallet, balance_wallet, deposits, balance_deposits
