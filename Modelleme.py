

tarihler = pd.read_excel("data.xlsx")
tarihler.columns = ["Tarih","y"]


tarihler["AYIN_GUNU"] = tarihler.Tarih.dt.day
tarihler["HAFTANIN_GUNU"] = tarihler.Tarih.dt.weekday
tarihler["HAFTAICI_FLAG"] = np.where(tarihler.Tarih.dt.weekday.isin([5, 6]), 0, 1)
tarihler["AY_15_FLAG"] = np.where(tarihler.Tarih.dt.day == 15, 1, 0)

turkey_holidays = holidays.Turkey()
holiday_liste = []
for i in range(tarihler.shape[0]):
    holiday_liste.append(
    np.where(date(tarihler.Tarih[i].year, tarihler.Tarih[i].month, tarihler.Tarih[i].day) in turkey_holidays, 1,
                     0))

tarihler["Holiday_Flag"] = holiday_liste
tarihler["Holiday_Flag"] = tarihler["Holiday_Flag"].astype("int64")
tarihler["SUBAT_FLAG"] = np.where(tarihler.Tarih.dt.month == 2, 1, 0)

tarihler.set_index("Tarih",inplace=True)


train_data = tarihler.loc["2017-01-01":"2020-12-31",:]
train_data_x = train_data.drop("y",axis=1)
train_data_y = train_data.y


test_data = tarihler.loc["2021-01-01":,:]
test_data_x = test_data.drop("y",axis=1)
test_data_y = test_data.y


from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error
sarima = SARIMAX(endog=train_data_y,exog= train_data_x,order= (2,0,1),seasonal_order=(0,1,1,7))

#sarima = SARIMAX(endog=train_data_y,exog= train_data_x,order= (2,0,1),seasonal_order=(1,1,1,7))

result = sarima.fit()

display(result.summary())


plt.figure(figsize=(12,8))
train_tahminler = result.predict(start=0,
               end=len(train_data_y)-1,
               exog=train_data_x)

train_tahminler.plot(label="Predictions")
plt.plot(train_data_y,label="Train Data")
plt.legend()
print("MEAN ABSOLUTE PERCENTAGE ERROR:",mean_absolute_error(train_data_y.values,train_tahminler) / train_data_y.mean())


plt.figure(figsize=(12,8))
test_tahminler = result.predict(start=len(train_data_y),
               end=len(train_data_y)+len(test_data_y)-1,
               exog=test_data_x)

test_tahminler.plot(label="Tahminler")
plt.plot(test_data_y,label="Test Data")
plt.xlabel("Zaman Periyodu")
plt.title("2021 Yılı Model Tahminleri")
plt.ylabel("Günlük Arama Adetleri")
plt.legend()

print("MEAN ABSOLUTE PERCENTAGE ERROR:",mean_absolute_error(test_data_y.values,test_tahminler) / test_data_y.mean())

from statsmodels.tsa.statespace.sarimax import SARIMAXResults
result.save("Cagri_Tahminleme_Model.pkl",remove_data=False)
