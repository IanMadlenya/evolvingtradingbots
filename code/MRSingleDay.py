"""
Class for simulating and measuring performance over a single day on a mean reversion
strategy.
"""

import pandas as pd
from pandas.stats.moments import rolling_mean
from Tools import average_true_range, snf, test_fixed_stop_target, test_fixed_bar_exit

DATA_DIR = "/Users/peterharrington/Documents/GitHub/evolvingtradingbots/data/min/"


class MRSingleDay():
    def __init__(self, fn, a, b):
        self.a = a             # paramater to scale the ATR
        self.mean_days = b     # number of days over which to take the mean
        self.df = pd.read_csv(DATA_DIR + fn, index_col='Date', parse_dates=True, na_values=['nan'])

    def calc_returns(self):
        """Calculates returns """
        self.df["ATR"] = average_true_range(self.df)

        mean = rolling_mean(self.df["Adj Close"], self.mean_days)
        self.df["plus"] = mean + self.a * self.df["ATR"]
        self.df["minus"] = mean - self.a * self.df["ATR"]

        self.df["position"] = 0.0

        # figure out when the close is higher than the plus
        # delay by one period
        low_triggered = snf(self.df["Adj Close"] > self.df["plus"])
        num_low_entries = low_triggered.sum()

        # set the position (the period following)
        self.df.loc[low_triggered, "position"] = -1.0

        # figure out when the close is less than plus
        high_triggered = snf(self.df["Adj Close"] < self.df["minus"])
        num_high_entries = high_triggered.sum()
        self.df.loc[high_triggered, "position"] = 1.0
        entries = num_high_entries + num_low_entries

        self.df["period_returns"] = self.df["Adj Close"] - self.df["Adj Close"].shift(1)

        # now here we can calculate the exit based on different strategies
        return test_fixed_stop_target(self.df)  # may want to pass this function in, in a functional way
        #return test_fixed_bar_exit(self.df)


if __name__ == '__main__':
    print "all done boss"