import os

from dotenv import load_dotenv
import fire

from trade_algos.simple import SimpleAlgorithm
from trade_algos.copycat import CopyCatAlgorithm

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

def test(symbol, qty, gain, loss):
    print(f'{symbol} {qty} {gain} {loss}')
    print(API_KEY)
    print(API_SECRET)
    
if __name__ == "__main__":
    fire.Fire()