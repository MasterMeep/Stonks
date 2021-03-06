import streamlit as st
from datetime import date

import yfinance as yf
from plotly import graph_objs as go
import json

START = "2018-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Stonks")

data = json.load(open('tickers.json'))
stocks = tuple(map(lambda x: x['Symbol'], data))

selected_stock = st.selectbox("Select stock for prediction", stocks)
current_period = st.select_slider(
     'Select a peiod of time',
     options=['5d',"1mo","3mo","6mo","1y",'2y','5y','10y','max'])


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

tickers_to_name = {x['Symbol']:x["Name"] for x in json.load(open("tickers.json"))}

st.title(f"Open/Close Data for {tickers_to_name[selected_stock]}")
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
