import os
import json

from dotenv import load_dotenv
import fire
from trade_algos import BaseAlgorithm
import arrow

from trade_algos.simple import SimpleAlgorithm
from trade_algos.copycat import CopyCatAlgorithm
from ark_wrapper import Ark

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

def simple(symbol: str, qty: int = 1, gain: float = 1, loss: float = 1):
    simple_algo = SimpleAlgorithm(API_KEY, API_SECRET)

    simple_algo.add_symbol(symbol, qty=qty)

    simple_algo.set_max_loss(symbol, loss)
    simple_algo.set_min_gain(symbol, gain)
    
    simple_algo.run()

def copycat(symbol: str, daily_budget_percentage: float, min_bal: float):
    copycat = CopyCatAlgorithm(API_KEY, API_SECRET)

    copycat.set_etf_symbol(symbol)
    copycat.set_daily_budget_percent(daily_budget_percentage)
    copycat.set_min_balance(min_bal)

    copycat.run()

def ark(symbol: str, mode: str, start_date: str = None, end_date: str = None, limit: int = 100):
    ark = Ark()
    if mode == 'holdings':
        print(json.dumps(ark.get_etf_holdings(symbol, start_date, end_date, limit), indent=4))

    elif mode == 'trades':
        print(json.dumps(ark.get_etf_trades(symbol, start_date, end_date, limit), indent=4))

    else:
        print('Invalid mode')

def historical(symbol: str, timeframe: str = 'day', limit: int = 100):
    base = BaseAlgorithm(API_KEY, API_SECRET)
    bars = base.api.get_barset(symbol, timeframe, limit)
    for bar in bars[symbol]:
        timestamp = arrow.get(bar.t)
        print(f'Date: {timestamp.format("YYYY-MM-DD hh:mm:ss")} Open: {bar.o} Close: {bar.c} High: {bar.h} Low: {bar.l} Volume: {bar.v}')

def current(symbol: str):
    base = BaseAlgorithm(API_KEY, API_SECRET)
    barset = base.api.get_barset(symbol, 'minute', limit=1)
    print(barset[symbol][0].c)

def yesterday(symbol: str):
    base = BaseAlgorithm(API_KEY, API_SECRET)
    print(base.get_yesterday_price(symbol))


def test(symbol, qty, gain, loss):
    print(f'{symbol} {qty} {gain} {loss}')
    print(API_KEY)
    print(API_SECRET)
    
if __name__ == "__main__":
    fire.Fire()