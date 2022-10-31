import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import pydeck as pdk

def get_crypto_prices(symbol, start, end):
    api_key = '7d9fd462584daa7dbbf18aa0b756aea7'
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
            prices.append('NaN')
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
    ["Homepage", "Current Cryptocurrency Data", "Historical Data", "Cryptocurrency Conversions"]
)

if add_selectbox == "Current Cryptocurrency Data":
    st.header("Current Cryptocurrency Data")
    desired_coin = st.text_input("Input the Coin you want to examine here (Example: BTC):")
    todays_date = st.date_input("Please select today's date:")
    end_date = todays_date
    if desired_coin:
        st.table(get_crypto_prices(desired_coin, todays_date, end_date))

elif add_selectbox == "Historical Data":
    st.header("Historical Cryptocurrency Data")
    desired_coin = st.text_input("Input the Coin you want to examine here (Example: BTC):")
    start_date = st.text_input("Enter the date you want to start to analyze the currency at in the format 'YYYY-MM-DD':")
    end_date = st.text_input("Enter the end date you want to analyze the currency in the format 'YYYY-MM-DD':")
    if desired_coin and start_date and end_date:
        st.table(get_crypto_prices(desired_coin, start_date, end_date))

elif add_selectbox == "Cryptocurrency Conversions":
    st.header("Cryptocurrency Conversions")
    st.subheader("Map- Crypto Capitals")
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

    capitals = st.selectbox('Select a country to view cryptocurrency prices',
                            ["Brazil", "Colombia", "India", "Indonesia", "Kenya", "Nigeria",
                             "Pakistan", "Phillipines", "Russia", "South Africa", "Thailand",
                            "Ukraine", "United Kingdom", "United States", "Venezuela", "Vietnam"])

else:
    st.header("CAP 4104 - Developed by Adriel Molerio & Ashley Royce")
    st.text("This page has been developed to share information about cryptocurrency data, both historical and current.")
    st.image("media/Coins.jpg")
    st.caption("Source: https://www.finextra.com/the-long-read/523/the-future-of-digital-banking-in-north-america-chain-reactions---cryptocurrency-vs-remittances")