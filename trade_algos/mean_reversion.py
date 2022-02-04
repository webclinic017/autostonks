from collections import OrderedDict
from typing import List
import json


import arrow
from alpaca_trade_api import TimeFrame, TimeFrameUnit
import requests

from . import BaseAlgorithm

class MeanReversionAlgorithm(BaseAlgorithm):

    def set_tickers(self, tickers: List[str]):
        self.tickers = tickers

    def mean(self, symbols: List[str], timeframe: str = 'month'):
        alpaca_timeframe = TimeFrame(1, TimeFrameUnit.Hour)
        start_date = arrow.now().shift(months=-1)
        if timeframe == 'day':
            start_date = arrow.now().shift(days=-1)
        if timeframe == 'week':
            start_date = arrow.now().shift(weeks=-1)
        today = arrow.now().shift(minutes=-15)
        try:
            bars = self.api.get_bars(symbols, alpaca_timeframe, start=start_date.isoformat(), end=today.isoformat(), limit=10000)
        except requests.exceptions.HTTPError as e:
            print('HTTPError: {}'.format(e))
            return {}
        # bars for multiple symbols are grouped in the same list
        # create an object with each symbol as a key
        # and the list of bars as the value
        # e.g. {'TSLA': [bar1, bar2, bar3], 'AAPL': [bar1, bar2, bar3]}
        bars_by_symbol = {}
        changes_by_symbol = {}
        for bar in bars:
            if bar.S in bars_by_symbol:
                bars_by_symbol[bar.S].append(bar)
            else:
                bars_by_symbol[bar.S] = [bar]
        
        # sort the bars by time
        for symbol in bars_by_symbol:
            bars_by_symbol[symbol].sort(key=lambda bar: bar.t)
            changes_by_symbol[symbol] = []
            for i in range(1, len(bars_by_symbol[symbol])):
                changes_by_symbol[symbol].append(bars_by_symbol[symbol][i].c - bars_by_symbol[symbol][i-1].c)
        
        # calculate the mean of the changes
        means = {}
        for symbol in changes_by_symbol:
            means[symbol] = sum(changes_by_symbol[symbol]) / len(changes_by_symbol[symbol])

        return means

    def run(self, tickers: List[str], output: bool = False):

        print('Initialzing Mean Reversion Algorithm')
        print('Getting Tickers')
        self.set_tickers(tickers)

        values = {}

        print('Running first time analysis.....')
        for ticker in self.tickers:
            print('Analyzing {}'.format(ticker))
            roc = self.mean([ticker])
            if roc:
                values[ticker] = roc[ticker]

        sorted_values = OrderedDict(sorted(values.items(), key=lambda x: x[1], reverse=True))
        
        if output:
            # output to json file
            with open('mean_reversion.json', 'w') as outfile:
                json.dump(sorted_values, outfile, indent=4)
        
        