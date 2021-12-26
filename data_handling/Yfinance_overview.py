# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 20:45:57 2021

@author: Randy666
"""
import datetime as dt
import numpy as np
import sklearn
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from yahoofinancials import YahooFinancials #.JSON data structure

stocks = ['600600.SS','000858.SZ','600197.SS']


start = dt.datetime.today()-dt.timedelta(60);
end = dt.datetime.today();

all_data = {};
cl_prices = pd.DataFrame();

for ticker in stocks:
    cl_prices[ticker] = yf.download(ticker,start,end)['Adj Close']
    
    
for ticker in stocks:
    all_data[ticker] = yf.download(ticker,start,end)
    
    
