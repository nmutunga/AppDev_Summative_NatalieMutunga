import numpy as np
import pickle
import requests
import pandas as pd
import calendar
import datetime

#use the urls to get back the weather data in json form
url = "http://www.7timer.info/bin/api.pl?lon=142.158&lat=-19.921&product=meteo&output=json"
data_1 = requests.get(url).json()

url2 = "http://www.7timer.info/bin/meteo.php?lon=8.6&lat=53.6&ac=0&unit=metric&output=json&tzshift=0"
data_2 = requests.get(url2).json()

url3 = "http://www.7timer.info/bin/api.pl?lon=142.158&lat=-19.921&product=civillight&output=json"
data_3 = requests.get(url3).json()

weather_dataframe = pd.DataFrame()  # Create an empty dataframe

# Create empty lists to store the predictor variables
dates = []
temperature = []
cloudcover = []
rainfall = []
windspeed = []
winddirection = []
j = 0
k = 0
l = 0

#use for loops the get the variables we need for our model
for i in range(0,4):
    cloud = data_1['dataseries'][j]['cloudcover']
    cloudcover.append(cloud)
    rain = data_1['dataseries'][j]["prec_amount"]
    rainfall.append(rain)
    temp = data_1['dataseries'][j]['temp2m']
    temperature.append(temp)
    j = j + 7

for i in range(0,4):
    speed = data_2['dataseries'][k]['wind_profile'][0]['direction']
    windspeed.append(speed)
    direction = data_2['dataseries'][k]['wind_profile'][0]['speed']
    winddirection.append(direction)
    k = k + 7

for i in range(0,4):
    date = data_3['dataseries'][l]['date']
    dates.append(date)
    l = l + 1

# Write lists to DF
weather_dataframe['date'] = dates
weather_dataframe['cloud'] = cloudcover
weather_dataframe['temp'] = temperature
weather_dataframe['windspeed'] = windspeed
weather_dataframe['direction'] = winddirection
weather_dataframe['rainfall'] = rainfall

# # Convert timestamp to datetime
weather_dataframe['date'] = pd.to_datetime(weather_dataframe['date'], format='%Y%m%d')
weather_dataframe['day'] = weather_dataframe['date'].dt.day

# print(weather_dataframe)
# print(weather_dataframe.dtypes)
