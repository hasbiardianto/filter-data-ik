import streamlit as st
import pandas as pd
import numpy as np
from charset_normalizer import from_path
 
st.set_page_config('Filter Data Index Kasus')


data = st.file_uploader('Upload Data')

if data:
    df_data = pd.read_excel(data)
    df_data.rename(columns={'person_id' : 'Person ID SITB'}, inplace=True)
    st.dataframe(df_data)

filter = st.file_uploader('Filter Data')

if filter:
    df_filter = pd.read_excel(filter, header=3)
    st.dataframe(df_filter)

if filter and data :
    # Mengambil set data Person ID SITB yang ada di file filter
    set_filter_ids = set(df_filter['Person ID SITB'])

    # Memilih baris-baris dari data utama yang Person ID SITB-nya tidak ada di filter
    df_filtered_data = df_data[~df_data['Person ID SITB'].isin(set_filter_ids)]

    st.dataframe(df_filtered_data)