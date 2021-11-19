from alpaca_trade_api.rest import REST, APIError
import arrow

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

    def get_number_of_shares(self, symbol: str):
        try:
            return float(self.api.get_position(symbol).qty)
        except APIError:
            return 0
    
    def has_traded_today(self):
        # get the now timestamp
        now = arrow.now().format('YYYY-MM-DD')
        # get all orders after the now timestamp
        orders = self.api.list_orders(after=now, status='closed', limit=500)

        clock = self.api.get_clock()
        
        return len(orders) > 0 and clock.is_open

    def get_value_of_shares(self, symbol: str):
        return self.get_number_of_shares(symbol) * self.get_current_price(symbol)

    def get_account_value(self):
        return self.api.get_account().portfolio_value

    def get_account_cash(self):
        return float(self.api.get_account().cash)
    
    def get_account_buying_power(self):
        return float(self.api.get_account().buying_power)

    def get_account_equity(self):
        return float(self.api.get_account().equity)

    def get_current_price(self, symbol: str):
        return float(self.api.get_barset(symbol, 'minute', limit=1)[symbol][0].c)
    
    def get_yesterday_price(self, symbol: str):
        barset = self.api.get_barset(symbol, 'day', limit=2)
        return float(barset[symbol][-1].c)

    def clear_account_orders(self):
        orders = self.api.list_orders(status='open')
        for order in orders:
            self.api.cancel_order(order.id)

    def place_notional_order(self, symbol: str, price: float):
        return self.api.submit_order(
            symbol=symbol,
            notional=price,
            side='buy',
            type='market',
            time_in_force='day'
        )

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

    def sell_notional_order(self, symbol: str, price: float):
        return self.api.submit_order(
            symbol=symbol,
            notional=price,
            side='sell',
            type='market',
            time_in_force='day'
        )

    def run(self):
        pass