from alpaca_trade_api.rest import REST

class BaseAlgorithm:
    def __init__(self, API_KEY: str, API_SECRET: str, base_url: str='https://paper-api.alpaca.markets', api_version: str='v2'):
        self.api = REST(API_KEY, API_SECRET, base_url=base_url, api_version=api_version)
        self.symbols = {}
        self.holding_count = 0

    def add_symbol(self, symbol: str, **kwargs):
        self.symbols[symbol] = kwargs or {}

    def get_symbol(self, symbol: str):
        return self.symbols[symbol]

    def get_symbols(self):
        return self.symbols.keys()

    def get_account_value(self):
        return self.api.get_account().portfolio_value

    def get_account_cash(self):
        return self.api.get_account().cash
    
    def get_account_buying_power(self):
        return self.api.get_account().buying_power

    def get_account_equity(self):
        return self.api.get_account().equity

    def get_current_price(self, symbol: str):
        return self.api.get_barset(symbol, 'minute', limit=1)[symbol][0].c

    def clear_account_orders(self):
        orders = self.api.list_orders(status='all')
        for order in orders:
            self.api.cancel_order(order.id)

    def place_buy_order(self, symbol: str, qty: int):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='day'
        )

    def place_sell_order(self, symbol: str, qty: int):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='day'
        )

    def place_limit_buy_order(self, symbol: str, qty: int, limit_price: float):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='limit',
            time_in_force='day',
            limit_price=limit_price
        )

    def place_limit_sell_order(self, symbol: str, qty: int, limit_price: float):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='limit',
            time_in_force='day',
            limit_price=limit_price
        )

    def place_stop_buy_order(self, symbol: str, qty: int, stop_price: float):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='stop',
            time_in_force='day',
            stop_price=stop_price
        )

    def place_stop_sell_order(self, symbol: str, qty: int, stop_price: float):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='stop',
            time_in_force='day',
            stop_price=stop_price
        )

    def run(self):
        pass