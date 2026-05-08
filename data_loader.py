import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("products.csv")
    # Clean the tags just in case
    df['tags'] = df['tags'].fillna('')
    return df