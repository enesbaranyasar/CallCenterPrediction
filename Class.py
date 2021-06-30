from call_Center import forecast_function,exog_variable_creator

class TimeSeries:
    def __init__(self,baslangic,bitis):
        self.baslangic = baslangic
        self.bitis = bitis

    def predict(self):
        return forecast_function(exog_data=exog_variable_creator(self.bitis),baslangic_tarihi=self.baslangic)



