"""This class creates plots for the reports"""

import matplotlib.pyplot as plt
import pandas as pd

DATA_DIR = "/Users/peterharrington/Documents/GitHub/evolvingtradingbots/data/min/"
CODE_DIR = "/Users/peterharrington/Documents/GitHub/evolvingtradingbots/code/"

def plot_single_day():
    """Choose a day's data and plot it"""
    df = pd.read_csv(DATA_DIR + "ZS201507_20150702.csv", index_col='Date', parse_dates=True, na_values=['nan'])
    df["Adj Close"].plot()
    plt.xlabel("time (PST)")
    plt.ylabel("Settlement Price ($0.01)")
    plt.title("Soybeans Futures Prices on 2015/07/02")
    plt.show()

def plot_cum_results():
    data = []; cum_data = [0]
    sum = 0
    #fr = open("SA_winratio_results.txt")
    fr = open("SA_avgprofit_results.txt")
    #fr = open("SA_results.txt")
    for line in fr.readlines():
        la = line.split("\t")
        curr_val = float(la[4])
        data.append(curr_val)
        cum_data.append(sum + curr_val)

        sum += curr_val

    plt.plot(cum_data)
    plt.xlabel("trading day")
    plt.ylabel("Cumulative Return ($0.01)   ")
    plt.title("Cumulative Returns")
    plt.show()

def plot_cum_results2():
    df = pd.read_csv(CODE_DIR + "SA_GA_cum.csv")

    df["Genetic Algorithm"].plot(legend=True)
    df["Simulated Annealing"].plot(legend=True)
    plt.xlabel("trading day")
    plt.ylabel("Cumulative Return ($0.01)   ")
    plt.title("Cumulative Returns")
    plt.show()

if __name__ == '__main__':
    #plot_single_day()
    #plot_cum_results()
    plot_cum_results2()