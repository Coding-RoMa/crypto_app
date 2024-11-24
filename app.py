import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go
from datetime import date  # Import the date class
from ta.utils import dropna
from ta.volatility import BollingerBands

st.title("Market Dashboard Application")
st.sidebar.header("User Input")

def get_input():
    # Use date objects for default values
    symbol = st.sidebar.text_input("Symbol", "BTC-USD")
    start_date = st.sidebar.date_input("Start Date", date(2021, 1, 1)) 
    end_date = st.sidebar.date_input("End Date", date(2021, 12, 31))
    return symbol, start_date, end_date

def get_data(symbol, start_date, end_date):
    symbol = symbol.upper()
    if symbol:
        df = yf.download(symbol, start=start_date, end=end_date)
        df = df.dropna()  # Drop rows with missing values
    else:
        df = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close'])
    return df

# Unpack user inputs
symbol, start_date, end_date = get_input()
df = get_data(symbol, start_date, end_date)

if not df.empty and 'Adj Close' in df.columns:
    # Drop rows with missing values
    df = dropna(df)

    # Initialize Bollinger Bands Indicator
    indicator_bb = BollingerBands(close=df["Adj Close"], window=20, window_dev=2)

    # Add Bollinger Bands features to the DataFrame
    df['bb_mavg'] = indicator_bb.bollinger_mavg()  # Middle Band
    df['bb_high'] = indicator_bb.bollinger_hband()  # High Band
    df['bb_low'] = indicator_bb.bollinger_lband()  # Low Band

    # Visualization
    st.subheader("Bollinger Bands Chart")
    fig = go.Figure()

    # Add Adjusted Close Price Line
    fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'], mode='lines', name='Adj Close'))

    # Add Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df['bb_high'], mode='lines', name='BB High', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=df['bb_low'], mode='lines', name='BB Low', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['bb_mavg'], mode='lines', name='BB Mavg', line=dict(color='green')))

    # Update Layout
    fig.update_layout(
        title="Bollinger Bands with Adj Close Price",
        xaxis_title="Date",
        yaxis_title="Price",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig)
else:
    st.write("No valid data available for the selected date range or symbol.")

st.subheader("Historical Prices")
st.write(df)

st.subheader("Data Statistics")
st.write(df.describe())
