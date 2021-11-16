import time

from . import BaseAlgorithm
class SimpleAlgorithm(BaseAlgorithm):
    '''
    Buys given stock or crypto. Set a max loss and a min gained. When min gained is hit, sell. When max loss is hit, sell.
    '''
    def set_min_gain(self, symbol: str, min_gain: float) -> None:
        self.symbols[symbol]['min_gain'] = min_gain

    def set_max_loss(self, symbol: str, max_loss: float) -> None:
        self.symbols[symbol]['max_loss'] = max_loss

    def set_buy_price(self, symbol: str, buy_price: float) -> None:
        self.symbols[symbol]['buy_price'] = buy_price

    def get_min_gain(self, symbol: str) -> float:
        return self.symbols[symbol]['min_gain']

    def get_max_loss(self, symbol: str) -> float:
        return self.symbols[symbol]['max_loss']

    def get_buy_price(self, symbol: str) -> float:
        return self.symbols[symbol]['buy_price']

    def run(self):
        # clear exising orders
        self.clear_account_orders()

        # get symbols
        symbols = self.get_symbols()

        # iterate through symbols
        for symbol in symbols:
            print(f"Buying {symbol}....")
            # get current price
            current_price = self.get_current_price(symbol)
            self.set_buy_price(symbol, current_price)

            # buy the symbol at current market price
            self.place_buy_order(symbol, self.symbols[symbol].get('qty', 1))
            self.holding_count += 1
            print(f'{symbol} bought at {current_price}')

        while self.holding_count > 0:
            # iterate through symbols
            for symbol in symbols:
                print('-' * 20)
                # get current price
                current_price = self.get_current_price(symbol)
                buy_price = self.get_buy_price(symbol)
                min_gain = self.get_min_gain(symbol)
                max_loss = self.get_max_loss(symbol)
                difference = (current_price - buy_price) * self.symbols[symbol].get('qty', 1)
                print(f'{symbol} current price: {current_price}')
                print(f'{symbol} buy price: {buy_price}')
                print(f'{symbol} difference: {round(difference, 2)}')
                if difference > min_gain:
                    # sell the symbol at current market price
                    self.place_sell_order(symbol, symbols.get('qty', 1))
                    self.holding_count -= 1
                    print(f'{symbol} sold at {current_price}')
                elif difference < max_loss:
                    # sell the symbol at current market price
                    self.place_sell_order(symbol, symbols.get('qty', 1))
                    self.holding_count -= 1
                    print(f'{symbol} sold at {current_price}')

            # wait a second
            time.sleep(1)