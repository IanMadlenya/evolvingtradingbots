import pandas as pd
from pandas.stats.moments import rolling_mean


# Original code of inefficient version: http://www.gbquant.com/?p=9
# the inefficient version was rewritten.
def calc_true_range(df):
    hilo = df["High"] - df["Low"]
    hiclo = abs(df["High"] - df["Close"].shift(1))
    loclo = abs(df["Low"] - df["Close"].shift(1))
    temp = pd.concat([hilo, hiclo, loclo], axis=1)

    return temp.max(axis=1)


def average_true_range(df, N=14):
    """calculates the ATR by taking a rolling mean over the true range."""
    true_range = calc_true_range(df)
    return rolling_mean(true_range, N)


def snf(df):
    """shift and fill, used to delay logical trading signals"""
    return df.shift(1).fillna(False)