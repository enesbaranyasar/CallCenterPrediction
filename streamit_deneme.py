# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 11:33:27 2021

@author: enesb
"""

from call_Center import forecast_function,exog_variable_creator
from Class import TimeSeries
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Çağrı Merkezi Tahminleme Modeli')

st.markdown("""
Bu uygulamada tahmin etmek istediğiniz aralığı belirtmeniz yeterli. 
\n ** Model size çıktıyı verecektir.**
""")

st.sidebar.header('Tahminlenmek Istenen Aralığı Giriniz')
selected_year = st.sidebar.selectbox('Baslangic Ayı', ["2021-04-01","2021-05-01","2021-06-01","2021-07-01","2021-08-01","2021-09-01","2021-10-01","2021-11-01","2021-12-01"])
selected_year_2 = st.sidebar.selectbox('Bitis Ayı',   ["2021-04-30","2021-05-31","2021-06-30","2021-07-31","2021-08-31","2021-09-30","2021-10-31","2021-11-30","2021-12-31"])

obje = TimeSeries(baslangic = selected_year,bitis = selected_year_2)
prediction = obje.predict()
output = prediction.astype("int64")

output_2 = output.copy()

new_format = "%Y-%m-%d"
output_2.index = output_2.index.strftime(new_format)

st.write(output_2)
st.dataframe(output_2)
st.line_chart(output)

help(st.line_chart)
def filedownload(df):
    csv = df.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="CagriMerkeziTahminleme.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(output), unsafe_allow_html=True)

