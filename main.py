import streamlit as st
import pandas as pd
import numpy as np
import requests

st.set_page_config(
    page_title="Project 2- Adriel Molerio & Ashley Royce",
    layout = "wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'About': '#Welcome to to our project #2 Page. Developed by Adriel Molerio & Ashley Royce'
    }
)

st.title("CryptoCurrency Information")

add_selectbox = st.sidebar.selectbox(
    "Select a Page",
    ["Homepage", "Current Cryptocurrency Data", "Historical Data", "Cryptocurrency Conversions"]
)

if add_selectbox == "Current Cryptocurrency Data":
    st.header("Current Cryptocurrency Data")

elif add_selectbox == "Historical Data":
    st.header("Historical Cryptocurrency Data")

elif add_selectbox == "Cryptocurrency Conversions":
    st.header("Cryptocurrency Conversions")

else:
    st.header("CAP 4104 - Developed by Adriel Molerio & Ashley Royce")
    st.text("This page has been developed to share information about cryptocurrency data, both historical and current.")
    st.image("media/Coins.jpg")
    st.caption("Source: https://www.finextra.com/the-long-read/523/the-future-of-digital-banking-in-north-america-chain-reactions---cryptocurrency-vs-remittances")