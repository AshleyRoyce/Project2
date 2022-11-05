import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import pydeck as pdk

def get_crypto_prices(symbol, start, end):
    api_key = '00f2a8f69b8c4ad6cf314cee14da7beb'
    series = pd.date_range(start, end)
    dates = []
    for i in range(len(series)):
        dates.append(str(series[i]))
    date_series = []
    for i in dates:
        date_series.append(i[:10])
    prices = []
    for date in date_series:
        try:
            api_url = f'http://api.coinlayer.com/{date}&symbols={symbol}?access_key={api_key}'
            raw = requests.get(api_url).json()
            val = []
            val.append(raw['rates'])
            price = val[0][f'{symbol}']
            prices.append(price)
        except:
            st.error('Invalid coin symbol entered', icon="🚨")
            prices.append('')
    df = pd.DataFrame(columns=['date', 'price'])
    df['date'] = series
    df['price'] = prices
    return df

st.set_page_config(
    page_title="Project 2- Adriel Molerio & Ashley Royce",
    layout = "wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'About': '#Welcome to to our CAP4104 Project #2 Page. Developed by Adriel Molerio & Ashley Royce'
    }
)

st.title("CryptoCurrency Information")

add_selectbox = st.sidebar.selectbox(
    "Select a Page",
    ["Homepage", "Current Cryptocurrency Data", "Historical Data", "Global Cryptocurrency Conversions"]
)

if add_selectbox == "Current Cryptocurrency Data":
    st.header("Current Cryptocurrency Data")
    desired_coin = st.text_input("Input the Coin you want to examine here (Example: BTC):")
    other_coin = st.checkbox("Do you want to look at another coin?")
    todays_date = st.date_input("Please select today's date:")
    end_date = todays_date
    coin1_df = None
    coin2_df = None
    if desired_coin:
        coin1_df = get_crypto_prices(desired_coin, todays_date, end_date)
        st.table(coin1_df)
    if other_coin:
        desired_coin2 = st.text_input("Input your second desired coin here:")
        coin2_df = get_crypto_prices(desired_coin2, todays_date, end_date)
        st.table(coin2_df)

    st.subheader("Cryptocurrency Comparisons")
    #chart_data = {
     #   'Coin': ['LTC', 'BNB', 'XMR', 'XRP', 'AAVE', 'BSV', 'ZEC'],
      #  'Price(USD)': [69.75, 353.28, 160.07, 163.18, 95.52, 49.06, 54.17]
    #}
    bar_chart_df = pd.merge(coin1_df, coin2_df, how="outer", on=['price'])
    st.bar_chart(bar_chart_df)
    st.text("Prices as of today")


elif add_selectbox == "Historical Data":
    st.header("Historical Cryptocurrency Data")
    desired_coin = st.text_input("Input the Coin you want to examine here (Example: BTC):")
    start_date = st.date_input("Enter the date you want to start to analyze the currency.")
    end_date = st.date_input("Enter the date you want to stop analyzing the currency.")
    if desired_coin and start_date and end_date:
        coin_df = get_crypto_prices(desired_coin, start_date, end_date)
        st.table(coin_df)
        st.line_chart(coin_df['price'])


elif add_selectbox == "Global Cryptocurrency Conversions":
    st.header("Global Cryptocurrency Conversions")
    st.subheader("Map- Top Countries by Cryptocurrency Ownership")
    if st.button('Click here to view map of top crypto-owning countries'):
        df = pd.read_csv("csv/Crypto_Capitals_2022.csv")

        zoom_lat = df["latitude"].mean()
        zoom_long = df["longitude"].mean()

        st.pydeck_chart(pdk.Deck(
            # map_style https://docs.mapbox.com/api/maps/styles/
            map_style='mapbox://styles/mapbox/light-v10',
            initial_view_state=pdk.ViewState(
                latitude=zoom_lat,
                longitude=zoom_long,
                zoom=0.5,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[longitude, latitude]',
                    get_color='[26, 255, 0, 160]',
                    get_radius=150000,
                    pickable=True,
                ),
            ],
            tooltip={
                "html": "{name} <br/> % of population owning crypto: {percent}% <br/>",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }
        ))
        st.info('Statistical information displayed in map collected in 2021 by TripleA', icon="ℹ️")

    st.subheader("Cryptocurrency Converter by Country")
    coin = st.radio("Choose a Cryptopcurrency",
                    options=["Bitcoin", "Ethereum", "Litecoin"])

    if coin == "Bitcoin":
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
        response = requests.get(url).json()
        btc_price = response["USD"]
        st.write("Current price of Bitcoin in US$ {}".format(btc_price))

    elif coin == "Ethereum":
        url = "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,JPY,EUR"
        response = requests.get(url).json()
        btc_price = response["USD"]
        st.write("Current price of Ethereum in US$ {}".format(btc_price))

    elif coin == "Litecoin":
        url = "https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,JPY,EUR"
        response = requests.get(url).json()
        btc_price = response["USD"]
        st.write("Current price of Litecoin in US$ {}".format(btc_price))

    capital = st.selectbox('Select a country to convert cryptocurrency prices',
                               ["Brazil", "Colombia", "India", "Indonesia", "Kenya", "Nigeria",
                                "Pakistan", "Philippines", "Russia", "South Africa", "Thailand",
                                "Ukraine", "United Kingdom", "Venezuela", "Vietnam"])

    if coin and capital == "Brazil":
        coin_price = (btc_price * 5.05)
        st.write("Current price of " + coin + " in BRL is: " + str(round(coin_price, 2)))

    if coin and capital == "Colombia":
        coin_price = (btc_price * 4974.21)
        st.write("Current price of " + coin + " in COP is: " + str(round(coin_price, 2)))

    if coin and capital == "India":
        coin_price = (btc_price * 81.98)
        st.write("Current price of " + coin + " in INR is: " + str(round(coin_price, 2)))

    if coin and capital == "Indonesia":
        coin_price = (btc_price * 15614.60)
        st.write("Current price of " + coin + " in IDR is: " + str(round(coin_price, 2)))

    if coin and capital == "Kenya":
        coin_price = (btc_price * 119.23)
        st.write("Current price of " + coin + " in KES is: " + str(round(coin_price, 2)))

    if coin and capital == "Nigeria":
        coin_price = (btc_price * 439.38)
        st.write("Current price of " + coin + " in NGN is: " + str(round(coin_price, 2)))

    if coin and capital == "Pakistan":
        coin_price = (btc_price * 217.86)
        st.write("Current price of " + coin + " in PKR is: " + str(round(coin_price, 2)))

    if coin and capital == "Philippines":
        coin_price = (btc_price * 58.33)
        st.write("Current price of " + coin + " in PHP is: " + str(round(coin_price, 2)))

    if coin and capital == "Russia":
        coin_price = (btc_price * 62.00)
        st.write("Current price of " + coin + " in RUB is: " + str(round(coin_price, 2)))

    if coin and capital == "South Africa":
        coin_price = (btc_price * 17.90)
        st.write("Current price of " + coin + " in ZAR is: " + str(round(coin_price, 2)))

    if coin and capital == "Thailand":
        coin_price = (btc_price * 37.29)
        st.write("Current price of " + coin + " in THB is: " + str(round(coin_price, 2)))

    if coin and capital == "Ukraine":
        coin_price = (btc_price * 36.06)
        st.write("Current price of " + coin + " in UAH is: " + str(round(coin_price, 2)))

    if coin and capital == "United Kingdom":
        coin_price = (btc_price * 0.88)
        st.write("Current price of " + coin + " in GBP is: " + str(round(coin_price, 2)))

    if coin and capital == "Venezuela":
        coin_price = (btc_price * 8.63545)
        st.write("Current price of " + coin + " in VES is: " + str(round(coin_price, 2)))

    if coin and capital == "Vietnam":
        coin_price = (btc_price * 24873.50)
        st.write("Current price of " + coin + " in VND is: " + str(round(coin_price, 2)))

else:
    st.header("CAP 4104 - Developed by Adriel Molerio & Ashley Royce")
    st.text("This page has been developed to share information about cryptocurrency data, both historical and current.")
    st.image("media/Coins.jpg")
    st.caption("Source: https://www.finextra.com/the-long-read/523/the-future-of-digital-banking-in-north-america-chain-reactions---cryptocurrency-vs-remittances")