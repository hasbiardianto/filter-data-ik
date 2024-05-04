import streamlit as st
import pandas as pd
import numpy as np
import io
import time
 
st.set_page_config('Filter Data Indeks Kasus')
st.title('Filter Data Indeks Kasus TBC')


st.header('Upload Data Baru')
data = st.file_uploader('Upload file Excel data indeks kasus yang belum difilter')

if data:
    on = st.toggle('Lihat Detail', key='ondata')
    df_data = pd.read_excel(data)
    df_data.rename(columns={'person_id' : 'Person ID SITB'}, inplace=True)
    if on:
        st.dataframe(df_data)

st.markdown("#")

st.header('Upload Data lama')
filter = st.file_uploader('Upload file Excel data indeks kasus yang sudah diinvestigasi kasus')

if filter:
    on = st.toggle('Lihat Detail', key='onfilter')
    df_filter = pd.read_excel(filter, header=0)
    if on:
        st.dataframe(df_filter)

st.markdown("#")


if filter and data :
    set_filter = st.button('Filter data..', type='secondary')
    if set_filter:
        with st.spinner('Tunggu Sebentar...'):
            msg = st.toast('Memproses data ...')
            time.sleep(1)
            buffer = io.BytesIO()

            msg.toast('Memfilter data...')
            time.sleep(1)
            set_filter_ids = set(df_filter['Person ID SITB'])
            df_filtered_data = df_data[~df_data['Person ID SITB'].isin(set_filter_ids)]

            # Mengganti nomor secara berurutan
            number = 1
            for index, row in df_filtered_data.iterrows():
                df_filtered_data.at[index, 'no'] = number
                number += 1
            df_filtered_data.reset_index(drop=True, inplace=True)
            st.dataframe(df_filtered_data)

            msg.toast('Membuat file excel...')
            time.sleep(1)
            date = time.gmtime()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)

            msg.toast('Data selesai dibuat')
            time.sleep(1)
            st.info('Data selesai dibuat...')
            download = st.download_button(
                label="Download data excel",
                data=buffer,
                file_name='data_ik_terfilter-{}{}{}.xlsx'.format(date.tm_mday, date.tm_mon, date.tm_year),
                mime='application/vnd.ms-excel'
            )