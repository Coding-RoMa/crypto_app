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
'''
def get_patterns():
    # Allow users to select one or more patterns from the list
    selected_patterns = st.sidebar.multiselect("Select Patterns", options=list(patterns.values())) # updating the current code - options=patterns)
    return selected_patterns


'''

# Unpack user inputs
symbol, start_date, end_date = get_input()
df = get_data(symbol, start_date, end_date)

'''
# Get user-selected patterns
selected_patterns = get_patterns()
'''

st.subheader("Historical Prices")
st.write(df)

st.subheader("Data Statistics")
st.write(df.describe())

st.subheader("Historical Price Chart - Adjusted Close Price")
st.line_chart(df['Adj Close'])

st.subheader("Volume")
st.bar_chart(df['Volume'])


#from where i got the patterns: 
# https://github.com/TA-Lib/ta-lib-python/blob/master/docs/func_groups/pattern_recognition.md#cdl2crows---two-crows

#here's another useful link: 
# https://github.com/TA-Lib/ta-lib/blob/main/docs/functions.md

'''
# Reverse the dictionary to map readable names back to codes
name_to_code = {v: k for k, v in patterns.items()}

# Convert selected patterns back to their corresponding codes
selected_codes = [name_to_code[name] for name in selected_patterns]
st.write("Corresponding Pattern Codes:")
st.write(selected_codes)


# Display selected patterns in the main app area
#st.write("You selected the following patterns:")
#st.write(selected_patterns)

'''

from ta.utils import dropna
from ta.volatility import BollingerBands
from ta import add_all_ta_features


# Clean NaN values (all columns)
df = dropna(df)

# Dynamically identify numerical columns
numerical_cols = df.select_dtypes(include=['number']).columns

# Ensure all numerical columns are 1D
for col in numerical_cols:
    df[col] = df[col].squeeze()

# Convert numerical columns to numeric explicitly (coerce errors to NaN)
df[numerical_cols] = df[numerical_cols].apply(pd.to_numeric, errors='coerce')

# Fill NaN values only in numerical columns
df[numerical_cols] = df[numerical_cols].fillna(0)

# Verify required columns exist for TA processing
required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f"Required columns are missing: {missing_cols}")

# Add TA features
df = add_all_ta_features(
    df, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True
)


# Initialize Bollinger Bands Indicator
indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)

# Add Bollinger Bands features
df['bb_bbm'] = indicator_bb.bollinger_mavg()
df['bb_bbh'] = indicator_bb.bollinger_hband()
df['bb_bbl'] = indicator_bb.bollinger_lband()

# Add Bollinger Band high indicator
df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

# Add Bollinger Band low indicator
df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()