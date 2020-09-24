import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from weather_data import weather_dataframe
# from Predictions import weather_predictions

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Hello World"

@app.route('/weather_data', methods=("POST", "GET"))
def weather():
    return render_template('weather.html',  tables=[weather_data.to_html(classes='data')], titles=weather_data.columns)

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        return render_template('index.html', shape=df.shape)
    return render_template('index.html')

# @app.route('/predict', methods=['GET','POST'])
# def predict():
#     return (render_template('index.html', tables =[weather_predictions.to_html(classes ='data' , index=False)]))
#
#
# @app.route('/calculate', methods=['POST'])
# def results():
#     data = request.get_json(force=True)
#     prediction = model.predict([np.array(list(data.values()))])
#
#     output = prediction[0]
#     return jsonify(output)
#
#
if __name__ == "__main__":
    app.run(debug=True)
