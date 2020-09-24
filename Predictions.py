import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from weather_data import weather_dataframe

app = Flask(__name__)

#read in our models with pickle
with open(r"C:\Users\Admin\Documents\AIIP\AppDev\Practice\model_solar.pkl", 'rb') as f_in:
    model_solar= pickle.load(f_in)
f_in.close()

with open(r"C:\Users\Admin\Documents\AIIP\AppDev\Practice\model_wind.pkl", 'rb') as file_in:
    model_wind = pickle.load(file_in)
file_in.close()

#drop the columns we didn't use in our model
solar_data = weather_dataframe.drop(['date','day','direction','windspeed'], axis=1)
wind_data = weather_dataframe.drop(['date','day','cloud','rainfall','temp'], axis=1)


#making predictions with the model
#store the values of the dataframe in an array
solar_features = solar_data.values
wind_features = wind_data.values
solar_prediction = model_solar.predict(solar_features)
wind_prediction = model_wind.predict(wind_features)

#store the predictions within our dataframe
weather_dataframe['solar_predictions']=solar_prediction
weather_dataframe['wind_predictions']= wind_prediction

#rearrange columns
columns = ['day','date','cloud','temp','rainfall','windspeed','direction','solar_predictions','wind_predictions']
df_predictions = weather_dataframe[columns]
print(df_predictions)

# print ('Power generated for the solar plant is {} and for the wind plant is {}'.format(solar_prediction,wind_prediction))
# print(weather_data)

