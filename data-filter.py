import streamlit as st
import pandas as pd
import numpy as np
import io
 
st.set_page_config('Filter Data Indeks Kasus')
st.title('Filter Data Indeks Kasus TBC')

st.header('Upload Data Baru')
data = st.file_uploader('Upload file Excel data indeks kasus yang belum difilter')

if data:
    df_data = pd.read_excel(data)
    df_data.rename(columns={'person_id' : 'Person ID SITB'}, inplace=True)
    st.dataframe(df_data)

st.header('Upload Data lama')
filter = st.file_uploader('Upload file Excel data indeks kasus yang sudah diinvestigasi kasus')

if filter:
    df_filter = pd.read_excel(filter, header=3)
    st.dataframe(df_filter)

if filter and data :
    buffer = io.BytesIO()
    set_filter_ids = set(df_filter['Person ID SITB'])
    df_filtered_data = df_data[~df_data['Person ID SITB'].isin(set_filter_ids)]

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)

    download = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='large_df.xlsx',
        mime='application/vnd.ms-excel'
    )