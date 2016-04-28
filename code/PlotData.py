"""This class creates plots for the reports"""

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = "/Users/peterharrington/Documents/GitHub/evolvingtradingbots/data/min/"

def plot_single_day():
    """Choose a day's data and plot it"""
    df = pd.read_csv(DATA_DIR + "ZS201507_20150702.csv", index_col='Date', parse_dates=True, na_values=['nan'])
    df["Adj Close"].plot()
    plt.xlabel("time (PST)")
    plt.ylabel("Settlement Price ($0.01)")
    plt.title("Soybeans Futures Prices on 2015/07/02")
    plt.show()

def plot_cum_results():
    data = []
    fr = open("SA_results.txt")
    for line in fr.readlines():
        la = line.strip().split("\t")
        print len(la)

        #data.append(float(la[4]))

    #plt.plot(data)
    #plt.show()

if __name__ == '__main__':
    #plot_single_day()
    plot_cum_results()