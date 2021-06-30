import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

from call_Center import forecast_function,exog_variable_creator
from Class import TimeSeries

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    tarih_features = [str(x) for x in request.form.values()]
    #final_features = [np.array(tarih_features)]
    obje = TimeSeries(baslangic = tarih_features[0],bitis = tarih_features[1])
    prediction = obje.predict()
    output = prediction.astype("int64")

#    output.to_excel("model_ciktisi_yeni.xlsx")
#    return render_template('index.html', tables=[output.to_html(classes='data')], titles=output.columns.values)

    return render_template('index.html', prediction_text='Predicted Call Amounts: {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = TimeSeries.predict(baslangic = data.values[0],bitis = data.values[1])
    output = prediction

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

