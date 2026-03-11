# 📊 Analyse par site
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Analyse par site", page_icon="📊", layout="wide")
from app import load_excel, concat_sites, DATA_PATH  # reuse cache & path

data_by_sheet = load_excel(DATA_PATH)
df = concat_sites(data_by_sheet)

site = st.selectbox('Site', sorted(df['Site'].dropna().unique()))
st.write(df[df['Site'] == site])
