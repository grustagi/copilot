#!/usr/bin/env python3
# Description: This file contains the code for the automated trading strategy.
#%% [markdown]
### Import Libraries
#%% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os
import sys
from tabulate import tabulate
# math functions

#%%
def rsi(df, period=7):
    """Return the RSI of a dataframe"""
    df['change'] = df['Close'].shift(1) - df['Close']
    df['gain'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['change'].apply(lambda x: -x if x < 0 else 0)
    df['avg_gain'] = df['gain'].rolling(period).mean()
    df['avg_loss'] = df['loss'].rolling(period).mean()
    df['rs'] = df['avg_gain'] / df['avg_loss']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    return df
#%%
def macd(df, period_long=26, period_short=12, period_signal=9):
    """Return the MACD of a dataframe"""
    df['ema_long'] = df['Close'].ewm(span=period_long).mean()
    df['ema_short'] = df['Close'].ewm(span=period_short).mean()
    df['macd'] = df['ema_short'] - df['ema_long']
    df['signal'] = df['macd'].ewm(span=period_signal).mean()
    return df
#%%
def bollinger_bands(df, period=20, std=2):
    """Return the Bollinger Bands of a dataframe"""
    df['ma'] = df['Close'].rolling(period).mean()
    df['bb_upper'] = df['ma'] + (df['Close'].rolling(period).std() * std)
    df['bb_lower'] = df['ma'] - (df['Close'].rolling(period).std() * std)
    return df
#%%
def stochastic_oscillator(df, period=14):
    """Return the Stochastic Oscillator of a dataframe"""
    df['l14'] = df['Low'].rolling(period).min()
    df['h14'] = df['High'].rolling(period).max()
    df['%k'] = 100 * ((df['Close'] - df['l14']) / (df['h14'] - df['l14']))
    df['%d'] = df['%k'].rolling(3).mean()
    return df
#%%
def trading_strategy(df):
    """Return the Trading Strategy of a dataframe"""
    """RSI Readings above 70 indicate overbought conditions, and below 30 suggest oversold conditions."""
    """StockRSI Readings above 80 indicate overbought conditions, and below 20 suggest oversold conditions."""
    df['buy'] = df.apply(lambda x: 1 if x['rsi'] < 30 and x['%k'] < 30 and x['macd'] > x['signal'] else 0, axis=1)
    df['sell'] = df.apply(lambda x: 1 if x['rsi'] > 70 and x['%k'] > 70 and x['macd'] < x['signal'] else 0, axis=1)
    return df
#%%
def trading_signals(df):
    """Return the Trading Signals of a dataframe"""
    df['positions'] = df['buy'] - df['sell']
    return df
#%%
def trading_returns(df):
    """Return the Trading Returns of a dataframe"""
    df['strategy'] = df['positions'].shift(1) * df['change']
    return df

# main function
def main(stock):
    ### Data Import
    #%% 
    # Import data from Yahoo Finance for 
    df = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1=1655749008&period2=1687285008&interval=1d&events=history&includeAdjustedClose=true')  
    # df = pd.read_csv('https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1655749008&period2=1687285008&interval=1d&events=history&includeAdjustedClose=true')
    #%%
    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    #%% [markdown]
    ### Data Exploration
    #%%
    # Show data
    df
    #%%
    # Show data types
    df.dtypes
    #%%
    # Show summary statistics
    df.describe()
    #%%
    # Show correlation matrix
    # df.corr()
    #%%
    # Show heatmap
    # sns.heatmap(df.corr(), annot=True)
    # plt.show()
    # #%% [markdown]
    #%% [markdown]
    ### Data Transformation
    #%%
    # Create new columns
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['quarter'] = df['Date'].dt.quarter
    #%% [markdown]
    ### Data Visualization
    #%%
    # Show line plot
    # df.plot(x='Date', y='Close', figsize=(10, 5))
    # plt.show()
    #%%
    # Show histogram
    # df['Close'].hist()
    # plt.show()
    #%%
    # Show box plot
    # df.boxplot(column=['Close'])
    # plt.show()
    # %%
    # Create a buy and sell trading strategy which makes positive returns from 2023-01-01 to 2023-05-05
    #%%
    # Create a buy and sell trading strategy from 2023-01-01 to 2023-05-05
    df = rsi(df)
    df = macd(df)
    df = bollinger_bands(df)
    df = stochastic_oscillator(df)
    df = trading_strategy(df)
    df = trading_signals(df)
    df = trading_returns(df)
    
    # add stock name to the df
    df['Stock'] = stock
    # df = df[df['Date'] >= '2023-01-01']
    # df = df[df['Date'] <= '2023-05-05']
    df.to_csv(f'{stock}.csv', index=False)
    return df

# end of main

#%%
# Import data
# https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1655749008&period2=1687285008&interval=1d&events=history&includeAdjustedClose=true
# df = pd.read_csv('data/Yahoo.AAPL.csv'
### Download data from Yahoo Finance
#%% [markdown]
# stock='ADANIENT.NS'
# 
# stocks = sys.argv[1].split(",")

# read niftymicrocap250 symbols from nse site
symbols_df = pd.read_csv("https://archives.nseindia.com/content/indices/ind_niftymicrocap250_list.csv")
symbols_df['Symbol'] = symbols_df['Symbol'].apply(lambda x: x + '.NS')
print(symbols_df)
stocks = symbols_df['Symbol'].to_list()
dfs = []
for stock in stocks:
    df = main(stock)
    dfs.append(df)

merged = pd.concat(dfs) # add ignore_index=True if appropriate
merged.to_csv('niftymicrocap250.NS.csv', index=False)