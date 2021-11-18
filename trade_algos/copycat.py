import time

from . import BaseAlgorithm
from ark_wrapper import Ark

class CopyCatAlgorithm(BaseAlgorithm):

    def set_daily_budget_percent(self, percent: float) -> None:
        self.daily_budget_percent = percent

    def set_min_balance(self, min_bal: float) -> None:
        self.min_bal = min_bal

    def set_etf_symbol(self, symbol: str = "ARKK") -> None:     # this is actually an ETF symbol; not a ticker.
        self.etf_symbol = symbol

    def run(self):
        ark = Ark()
        traded_today = False
        while True:
            clock = None
            try:
                clock = self.api.get_clock()
            except Exception as e:
                print(e)
                time.sleep(5)
                continue

            if traded_today:
                traded_today = False
                time.sleep(60 * 60 * 11)
                print("Sleeping until next data upload.")

            if not clock.is_open:
                time.sleep(10)
                continue

            print("Begin trading for today")    
            print(f'Getting ARK ETF Data for symbol {self.etf_symbol}...')
            yesterday_trades = ark.get_etf_trades(self.etf_symbol)
            yesterday_holdings = ark.get_etf_holdings(self.etf_symbol)
            
            self.daily_budget = (self.get_account_cash() - self.min_bal) * self.daily_budget_percent
            print(f'Daily budget: {self.daily_budget}')

            ark_purchases = {}              # value of shares purchased by ark
            ark_sells = {}                  # percentage of shares to sell
            calculated_purchases = {}       # dollars of shares to buy
            calculated_sells = {}           # dollars of shares to sell

            for trade in yesterday_trades['trades']:
                if trade['direction'] == "Buy":
                    # this gets cost
                    ark_purchases[trade['ticker']] = trade['shares'] * yesterday_holdings['trades']['share_price']
                if trade['direction'] == "Sell":
                    # this gets percentage of owned that was sold
                    ark_sells[trade['ticker']] = trade['shares'] / yesterday_holdings['trades']['shares']
                
            total_ark_purchased = 0         # total value of shares purchased by ark
            for purchase in ark_purchases:
                total_ark_purchased += ark_purchases[purchase]

            for symbol in ark_purchases:
                symbol_purchase_percentage = ark_purchases[symbol] / total_ark_purchased
                calculated_purchases[symbol] = self.daily_budget * symbol_purchase_percentage
                print(f"Planning to purchase {calculated_purchases[symbol]} of  {symbol}")      # print what we're planning to purchase

            for symbol in ark_sells:
                current_value = self.get_number_of_shares(symbol) * self.get_current_price(symbol)
                if not current_value:
                    continue
                calculated_sells[symbol] = current_value * ark_sells[symbol]
                print(f"Planning to sell {calculated_sells[symbol]} of {symbol}")               # print what we're planning to sell

            for purchase_symbol in calculated_purchases:
                if self.get_account_buying_power() < calculated_purchases[purchase_symbol]:
                    continue
                self.api.submit_order(
                    symbol=purchase_symbol,
                    qty=calculated_purchases[purchase_symbol],
                    side='buy',
                    type='market',
                    time_in_force='day',
                    order_class='bracket'
                )
                print(f"Sumbitted order to purchase {calculated_purchases[purchase_symbol]} of {purchase_symbol}")

            for sell_symbol in calculated_sells:
                if self.get_number_of_shares(sell_symbol) < calculated_sells[sell_symbol]:
                    continue
                self.api.submit_order(
                    symbol=sell_symbol,
                    qty=calculated_sells[sell_symbol],
                    side='sell',
                    type='market',
                    time_in_force='day',
                    order_class='bracket'
                )
                print(f"Sumbitted order to sell {calculated_sells[sell_symbol]} of {sell_symbol}")

            traded_today = True
            print("Done trading for the day.")