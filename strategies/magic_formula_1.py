# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 14:03:00 2021

@author: Randy666
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np



tickers = []
df_tickers = pd.read_csv('12-31.csv') #loading tickers with strong buy signals

#all below are Chinese stocks listed on the A-market
#the stocks are picked from the stock screener on TradingView.com with a 
#strong buy signal, sorted by market cap (descending order)
for i in range(len(df_tickers['Ticker'])):
    if len(str(df_tickers['Ticker'][i]))==6:
        
        if str(df_tickers['Ticker'][i])[0]=='6':
            
            tickers.append(str(df_tickers['Ticker'][i])+str('.SS'))
            
        else:
            tickers.append(str(df_tickers['Ticker'][i])+str('.SZ'))
        
tickers = tickers[0:50] #take the first 50 stickers
financial_dir = {}


for ticker in tickers:
    #getting balance sheet data from yahoo finance for the given ticker
    temp_dir = {}
    url = 'https://finance.yahoo.com/quote/'+ticker+'/balance-sheet?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
    
    #getting income statement data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/'+ticker+'/financials?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
    
    #getting cashflow statement data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/'+ticker+'/cash-flow?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.find_all("div", {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class" : "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[1]
    
    #getting key statistics data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/'+ticker+'/key-statistics?p='+ticker
    headers={'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,'html.parser')
    tabl = soup.findAll("table", {"class": "W(100%) Bdcl(c) "})
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2])>0:
                temp_dir[row.get_text(separator='|').split("|")[0]]=row.get_text(separator='|').split("|")[-1]    
    
    #combining all extracted information with the corresponding ticker
    financial_dir[ticker] = temp_dir



#storing information in pandas dataframe
combined_financials = pd.DataFrame(financial_dir)
combined_financials.dropna(how='all',axis=1,inplace=True) #dropping columns with all NaN values
tickers = combined_financials.columns #updating the tickers list based on only those tickers whose values were successfully extracted

# creating dataframe with relevant financial information for each stock using fundamental data
stats = ["Earnings before interest and taxes",
         "Market cap (intra-day)",
         "Net income applicable to common shares",
         "Total cash flow from operating activities",
         "Capital expenditure",
         "Total current assets",
         "Total current liabilities",
         "Property plant and equipment",
         "Total stockholder equity",
         "Long-term debt",
         "Preferred stock",
         "Minority interest",
         "Forward annual dividend yield"] # change as required

indx = ["EBIT","MarketCap","NetIncome","CashFlowOps","Capex","CurrAsset",
        "CurrLiab","PPE","BookValue","TotDebt","PrefStock","MinInterest","DivYield"]
all_stats = {}
for ticker in tickers:
    try:
        temp = combined_financials[ticker]
        ticker_stats = []
        for stat in stats:
            ticker_stats.append(temp.loc[stat])
        all_stats['{}'.format(ticker)] = ticker_stats
    except:
        print("can't read data for ",ticker)

all_stats_df = pd.DataFrame(all_stats,index=indx)


