import os

from dotenv import load_dotenv
import fire

from trade_algos.simple import SimpleAlgorithm

load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

def simple(symbol: str, qty: int = 1, gain: float = 1, loss: float = 1):
    simple_algo = SimpleAlgorithm(API_KEY, API_SECRET)

    simple_algo.add_symbol(symbol, qty=qty)

    simple_algo.set_max_loss(symbol, loss)
    simple_algo.set_min_gain(symbol, gain)
    
    simple_algo.run()


if __name__ == "__main__":
    fire.Fire()