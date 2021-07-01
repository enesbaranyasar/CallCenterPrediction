# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 11:33:27 2021

@author: enesb
"""

# from call_Center import forecast_function,exog_variable_creator
# from Class import TimeSeries
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import holidays
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from datetime import date


def exog_variable_creator(last_day):
    """
    Last Day "YYYY-MM-DD" formatında olmalı.

    Bu fonksiyon ile Ayın günü, haftanın günü, haftaiçi flag, ayın 15i flag,
    şubat ayı flag ve holiday flag değişkenleri oluşturulur.

    Kullanılan paketler : pandas,datetime,holiday
    """

    tarihler = pd.DataFrame(pd.date_range(start="2021-01-01", end=last_day), columns=["Tarih"])
    tarihler["AYIN_GUNU"] = tarihler.Tarih.dt.day
    tarihler["HAFTANIN_GUNU"] = tarihler.Tarih.dt.weekday
    tarihler["HAFTAICI_FLAG"] = np.where(tarihler.Tarih.dt.weekday.isin([5, 6]), 0, 1)
    tarihler["AY_15_FLAG"] = np.where(tarihler.Tarih.dt.day == 15, 1, 0)

    turkey_holidays = holidays.Turkey()
    turkey_holidays

    holiday_liste = []
    for i in range(tarihler.shape[0]):
        holiday_liste.append(
            np.where(date(tarihler.Tarih[i].year, tarihler.Tarih[i].month, tarihler.Tarih[i].day) in turkey_holidays, 1,
                     0))

    tarihler["Holiday_Flag"] = holiday_liste
    tarihler["Holiday_Flag"] = tarihler["Holiday_Flag"].astype("int64")
    tarihler["SUBAT_FLAG"] = np.where(tarihler.Tarih.dt.month == 2, 1, 0)

    tarihler.set_index("Tarih", inplace=True)
    return tarihler



def forecast_function(exog_data, baslangic_tarihi="2021-04-01"):
    """
    Tahminlemek istenilen zaman için yaratılan datayı exog_data parametresine girmek gerekiyor.
    Baslangic tarihi için de ne zamandan itibaren tahminler yapılacaksa o tarih girilecek.
    """
    start_number = 1461
    end_number = start_number + exog_data.shape[0] - 1

    loaded_model = SARIMAXResults.load("Cagri_Tahminleme_Model.pkl")

    predictions = loaded_model.predict(start=start_number, end=end_number, exog=exog_data)

    predictions = predictions.loc[baslangic_tarihi:]

    #plt.figure(figsize=(12, 8))
    #plt.xlabel("Time Period", fontsize=12)
    #plt.ylabel("Predictions", fontsize=12)
    #    plt.title("Number of Calls Expected from " + str(baslangic_tarihi) + " to " + str(exog_data.index.max()))
#    predictions.plot()

    return predictions


class TimeSeries:
    def __init__(self,baslangic,bitis):
        self.baslangic = baslangic
        self.bitis = bitis

    def predict(self):
        return forecast_function(exog_data=exog_variable_creator(self.bitis),baslangic_tarihi=self.baslangic)



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

