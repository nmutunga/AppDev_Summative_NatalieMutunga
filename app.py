import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from weather_data import weather_dataframe
from Predictions import final_dataframe
from Predictions import df_predictions
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import Dashboard
from twilio.rest import Client
import text


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = Dashboard.MyDashApp(server)

#Your Account Sid and Auth Token from twilio.com / console
account_sid = 'AC0adfaf15116c4650bd4020dd4d65a9b9'
auth_token = '1036e95afb7fa679169aedbcd463ab88'
client = Client(account_sid, auth_token)

#the data to be displayed by the text
output_text = final_dataframe['Total_Output(MW)'][0]
message = 'Total predicted power is {}'.format(output_text)

# @app.route("/", methods=["GET"])
# def index():
#     return flask.render_template("index.html")

@app.route('/weather_data', methods=("POST", "GET"))
def weather():
    return render_template('weather.html',  tables=[weather_dataframe.to_html(classes='data')], titles=weather_dataframe.columns)

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'))
        return render_template('index_2.html', shape=df.shape)
    return render_template('index_2.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    return (render_template('weather.html', tables =[df_predictions.to_html(classes ='data' , index=False)]))

@app.route('/message', methods=['POST', 'GET'])
def message():
    message_body = client.messages.create(
        body=message,
        from_='+12106101830',
        to='+254719671850'
    )
    return render_template("message.html", sms=message_body)




if __name__ == '__main__':
    app.run(port=5001, debug=True)
