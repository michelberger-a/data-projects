import yfinance as yf
import streamlit as st 
import pandas as pd
from datetime import date

st.write("""
# Simple Stock Price App
""")

stock = st.text_input("Stock:", "GOOGL")

st.write("Shown are the stock closing price and volume of: ")
st.write(f""" ### {stock} """)

# select ticker symbol
tickerSymbol = stock

# get the data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-1-1', end=date.today())
# will retrieve Open, High, Low, Close, volume, Dividends, Stock Splits

st.write("""
#### Closing Price
""")
st.line_chart(tickerDf.Close)

st.write("""
#### Trading Volume
         """)
st.line_chart(tickerDf.Volume)

st.write("""
#### Stock Splits
         """)
st.bar_chart(tickerDf["Stock Splits"])

# go to anaconda prompt (miniconda)
# conda activate dsi_participant - this is the environment
# use cd to get to folder location of py file
# streamlit run filename.py
# when it runs, it will appear as a local host
