import tinvest
from datetime import datetime
from pytz import timezone
from config import Tokens


def localize(d: datetime) -> datetime:
    return timezone('Europe/Moscow').localize(d)


def get_now() -> datetime:
    return localize(datetime.now())


class TinkoffAPI:
    """Обёртка для работы с API Тинькофф"""
    def __init__(self, api_secret: str, broker_account_id: str):
        self._client = tinvest.SyncClient(api_secret)
        self._broker_account_id = broker_account_id

    def get_portfolio_positions(self):
        """Получаем порфтель вида |Тикер|Имя|Валюта|Средняя цена|Кол-во|Возможная прибыль|,
        А также возвращаем курс доллара и незадействованные доллары в портфеле"""
        portfolio = {'stocks': [], 'usd_rub_currency': 0.00, 'free_usd': 0.00}
        response = self._client.get_portfolio(broker_account_id=self._broker_account_id)
        for position in response.payload.positions:
            ticker = position.ticker
            company = position.name
            balance = float(position.balance)
            currency = position.average_position_price.currency.value
            price_avg = float(position.average_position_price.value)
            profit = float(position.expected_yield.value)
            price_now = round((balance * price_avg + profit) / balance, 2)
            total = round(balance * price_now, 2)
            if ticker == 'USD000UTSTOM':
                portfolio['usd_rub_currency'] = price_now
                portfolio['free_usd'] = balance
            else:
                portfolio['stocks'].append([ticker, company, int(balance), currency, price_avg, price_now, total,
                                               profit])
        return portfolio

    def get_portfolio_positions_rub(self):
        """Получаем свободные рубли в портфеле"""
        response = self._client.get_portfolio_currencies(broker_account_id=self._broker_account_id)
        for position in response.payload.currencies:
            if position.currency.value == 'RUB':
                return float(position.balance)

    def get_all_operations(self, broker_account_started_at: datetime):
        """Возвращает операции в портфеле с указанной даты"""
        operations = {'dividend_usd': 0.00, 'dividend_rub': 0.00, 'pay_in_usd': 0.00, 'pay_in_rub': 0.00,
                      'pay_out_usd': 0.00, 'pay_out_rub': 0.00}

        from_ = localize(broker_account_started_at)
        now = get_now()
        response = self._client.get_operations(broker_account_id=self._broker_account_id, from_=from_, to=now)
        for position in response.payload.operations:
            if position.operation_type.value == 'Dividend':
                if position.currency.value == 'USD':
                    operations['dividend_usd'] = operations.get('dividend_usd') + float(position.payment)
                elif position.currency.value == 'RUB':
                    operations['dividend_rub'] = operations.get('dividend_rub') + float(position.payment)
            elif position.operation_type.value == 'PayIn':
                if position.currency.value == 'USD':
                    operations['pay_in_usd'] = operations.get('pay_in_usd') + float(position.payment)
                elif position.currency.value == 'RUB':
                    operations['pay_in_rub'] = operations.get('pay_in_rub') + float(position.payment)
            elif position.operation_type.value == 'PayOut':
                if position.currency.value == 'USD':
                    operations['pay_out_usd'] = operations.get('pay_out_usd') + float(position.payment)
                elif position.currency.value == 'RUB':
                    operations['pay_out_rub'] = operations.get('pay_out_rub') + float(position.payment)
        return operations


def build_collection(broker_account_id: str):
    """Собираем порфтель и статистику в коллекцию"""
    t = TinkoffAPI(Tokens.SECRET_KEY_TINKOFF, broker_account_id)
    portfolio = t.get_portfolio_positions()
    statistic = t.get_all_operations(datetime(2020, 1, 1))

    usd_rub_currency = portfolio.pop('usd_rub_currency')
    stocks = portfolio.pop('stocks')
    stocks_usd, stocks_rub = 0.00, 0.00
    for stock in stocks:
        if stock[3] == 'USD':
            stocks_usd += stock[6]
        elif stock[3] == 'RUB':
            stocks_rub += stock[6]
    stocks_sum = stocks_rub + stocks_usd * usd_rub_currency

    pay_in_usd = statistic.get('pay_in_usd')
    pay_in_rub = statistic.get('pay_in_rub')
    pay_in_sum = pay_in_rub + pay_in_usd * usd_rub_currency
    pay_out_usd = statistic.get('pay_out_usd')
    pay_out_rub = statistic.get('pay_out_rub')
    pay_out_sum = pay_out_rub + pay_out_usd * usd_rub_currency
    dividend_usd = statistic.get('dividend_usd')
    dividend_rub = statistic.get('dividend_rub')
    dividend_sum = dividend_rub + dividend_usd * usd_rub_currency
    free_usd = portfolio.pop('free_usd')
    free_rub = t.get_portfolio_positions_rub()
    free_sum = free_rub + free_usd * usd_rub_currency

    collection = {'pay_in_usd': pay_in_usd, 'pay_in_rub': pay_in_rub, 'pay_in_sum': pay_in_sum,
                  'pay_out_usd': pay_out_usd, 'pay_out_rub': pay_out_rub, 'pay_out_sum': pay_out_sum,
                  'dividend_usd': dividend_usd, 'dividend_rub': dividend_rub, 'dividend_sum': dividend_sum,
                  'free_usd': free_usd, 'free_rub': free_rub, 'free_sum': free_sum,
                  'stocks_usd': stocks_usd, 'stocks_rub': stocks_rub, 'stocks_sum': stocks_sum,
                  'profit': stocks_sum + free_sum - pay_out_sum - pay_in_sum}

    return {k: round(v, 2) for k, v in collection.items()}, stocks
