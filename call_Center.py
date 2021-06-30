import numpy as np
import pandas as pd
pd.set_option("display.max_columns",10)
import matplotlib.pyplot as plt
import seaborn as sns
import math
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error,mean_absolute_error
import random
import time
import warnings
warnings.filterwarnings("ignore")
import holidays
from datetime import date
from statsmodels.tsa.statespace.sarimax import SARIMAXResults


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


exog_variable_creator("2021-12-31")

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


forecast_function(exog_data=exog_variable_creator("2021-11-30"),
                  baslangic_tarihi="2021-10-01")






