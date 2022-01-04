# This file is based on: https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/app.py
import streamlit as st
from datetime import date

import yfinance as yf
from plotly import graph_objs as go

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stonks")

stocks = ("GOOGL", "TSLA", "AMZN", "FB")
selected_stock = st.selectbox("Select stock for prediction", stocks)
current_period = st.select_slider(
     'Select a color of the rainbow',
     options=['5d',"1mo","3mo","6mo","1y",'2y','5y','10y','ytd','max'])


@st.cache
def load_data(ticker):
    data = yf.download(ticker, period = current_period)
    data.reset_index(inplace=True)
    return data

load_state = st.text("Loading Data...")
data = load_data(selected_stock)
load_state.text("Loading Data... Done!")

load_state.text("")

def plot_data():
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="Close"))
    fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="Open"))

    fig.layout.update(xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)

st.title("Open/Close Data")
plot_data()

st.caption("Raw Data")
st.write(data)



st.title("Info")
info_state = st.text("Loading Data...")

stock_information = yf.Ticker(selected_stock).info

st.markdown(f"**Industry**: {stock_information['industry']}")
st.markdown(f"**Current Price**: ${'{:,}'.format(stock_information['currentPrice'])}")
st.markdown(f"**Yahoo Finance Recommendation**: {stock_information['recommendationKey']}")
st.markdown(f"**Gross Profits**: {'{:,}'.format(stock_information['grossProfits'])}")
st.markdown(f"**Enterprise Value**: {'{:,}'.format(stock_information['enterpriseValue'])}")
st.markdown(f"**Buisness Summary**: {stock_information['longBusinessSummary']}")

info_state.text("Loading Data... Done!")
info_state.text("")
