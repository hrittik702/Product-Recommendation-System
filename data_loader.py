import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("products.csv")
    df['tags'] = df['tags'].fillna('')     
    return df