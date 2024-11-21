import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from datetime import date  # Import the date class
from patterns import patterns


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

def get_patterns():
    # Allow users to select one or more patterns from the list
    selected_patterns = st.sidebar.multiselect("Select Patterns", options=patterns)
    return selected_patterns

# Unpack user inputs
symbol, start_date, end_date = get_input()
df = get_data(symbol, start_date, end_date)

# Get user-selected patterns
selected_patterns = get_patterns()

st.subheader("Historical Prices")
st.write(df)

st.subheader("Data Statistics")
st.write(df.describe())

st.subheader("Historical Price Chart - Adjusted Close Price")
st.line_chart(df['Adj Close'])

st.subheader("Volume")
st.bar_chart(df['Volume'])

# Display selected patterns in the main app area
st.write("You selected the following patterns:")
st.write(selected_patterns)
