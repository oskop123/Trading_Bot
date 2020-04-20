import datetime
import pandas as pd
import pandas_datareader as pdr
import numpy as np 
import matplotlib.pyplot as plt
import MovingAverageCrossStrategy
import Portfolio

if __name__ == "__main__":
    # Load daily bars of CDR from Yahoo Finance from the period of last 100 days
    symbol = 'CDR'
    time_start = datetime.datetime.today() - datetime.timedelta(days=200)
    time_stop = datetime.date.today()
    bars = pdr.DataReader(symbol, "yahoo", time_start, time_stop)

    