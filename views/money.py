from app import app
from flask import render_template
from flask_security import login_required
from services.stocks import build_collection
from services.crypto import build_collection_crypto
from config import Vars


@app.route('/stocks')
@login_required
def stocks():
    """ Страница. Ценные бумаги """
    stats_br, stocks_br, operations_usd_br, operations_usd_profit_br = build_collection('2001148671')
    stats_iis, stocks_iis, operations_usd_iis, operations_usd_profit_iis = build_collection('2004836843')
    operations_usd = operations_usd_br + operations_usd_iis
    operations_usd.sort(key=lambda k: k["date"])
    operations_usd_profit = round(operations_usd_profit_br + operations_usd_profit_iis, 2)
    return render_template('stocks.html', stats_br=stats_br, stocks_br=stocks_br,
                           stats_iis=stats_iis, stocks_iis=stocks_iis,
                           operations_usd_iis=operations_usd_iis, operations_usd=operations_usd,
                           operations_usd_profit=operations_usd_profit, tax_plus=int(Vars.TINKOFF_TAX_PLUS))


@app.route('/crypto')
@login_required
def crypto():
    """ Страница. Криптовалюта """
    wallet, balance_wallet, deposits, balance_deposits = build_collection_crypto()
    return render_template('crypto.html', wallet=wallet, balance_wallet=balance_wallet,
                           deposits=deposits, balance_deposits=balance_deposits)
