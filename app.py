
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

st.title("Market Dashboard Application")
st.sidebar.header("User Input")

def get_input():
    symbol = st.sidbar.text_input("Symbol", "BTC-USD")
    start_date = st.sidebar.date_input("Start Date", "2021-01-01")
    end_date = st.sidebar.date_input("End Date", "2021-12-31")

    return symbol, start_date, 

symbol, start_date, end_date = get_input()
