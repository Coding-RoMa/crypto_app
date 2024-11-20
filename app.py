import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from datetime import date  # Import the date class

st.title("Market Dashboard Application")
st.sidebar.header("User Input")

def get_input():
    # Use date objects for default values
    symbol = st.sidebar.text_input("Symbol", "BTC-USD")
    start_date = st.sidebar.date_input("Start Date", date(2021, 1, 1)) 
    # in the beginning i used the code shown in the course for dates, it was like this:
    # "Start Date", "2021-01-01"
    # But Streamlit doesn't accept this format, so i had to modify the code
    end_date = st.sidebar.date_input("End Date", date(2021, 12, 31))

    return symbol, start_date, end_date

def get_data(symbol, start_date, end_date):
    symbol = symbol.upper()
    if (symbol):
        df = yf.download(symbol, start=start_date, end=end_date)
    else:
        df = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close'])

    return df

# Unpack user inputs
symbol, start_date, end_date = get_input()
df = get_data(symbol, start_date, end_date)

st.subheader("Historical Prices")
st.write(df)

st.subheader("Data Statistics")
st.write(df.describe())
