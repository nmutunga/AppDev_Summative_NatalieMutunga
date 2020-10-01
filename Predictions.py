import numpy as np
import pandas as pd
import pickle
from weather_data import weather_dataframe

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

#now that we have our predictions, we can use the maintenance data to scale the expected output

#read in the maintenance csvs
wind_maintenance = pd.read_csv(r"C:\Users\Admin\Documents\AIIP\AppDev\Summative\wind_farm.csv")
solar_maintenance = pd.read_csv(r"C:\Users\Admin\Documents\AIIP\AppDev\Summative\solar_farm.csv")

#heck the columns
print(wind_maintenance.columns)
print(solar_maintenance.columns)

# Rename the columns of both dataframe
wind_maintenance_2 = wind_maintenance.rename(columns={'Date Of Month': 'day', 'Capacity Available': 'Capacity'},
                                             inplace=False)
solar_maintenance_2 = solar_maintenance.rename(columns={'Date Of Month': 'day', 'Capacity Available': 'Capacity'},
                                               inplace=False)

wind_maintenance_2['Capacity']=wind_maintenance_2['Capacity'].apply(lambda x:x/10)
solar_maintenance_2['Capacity']=solar_maintenance_2['Capacity'].apply(lambda x:x/10)
print(wind_maintenance_2)
print(solar_maintenance_2)

# merge the dataframes to work on the adjusted wind output
new_wind = pd.merge(df_predictions, wind_maintenance_2, on=['day'], how ='left')
new_wind['Capacity_filled'] = new_wind['Capacity'].fillna(value =1, inplace = False)
new_wind['Corrected_WindFarm_Output'] = new_wind['wind_predictions'] * new_wind['Capacity_filled']
final_wind = new_wind.drop(['Capacity'], axis=1)
print(final_wind)

 # merge the dataframes to work on the adjusted solar output
new_solar = pd.merge(df_predictions, solar_maintenance_2, on=['day'], how ='left')
new_solar['Capacity_filled'] = new_solar['Capacity'].fillna(value =1, inplace = False)
new_solar['Corrected_SolarFarm_Output'] = new_solar['solar_predictions'] * new_solar['Capacity_filled']
final_solar = new_solar.drop(['Capacity'], axis=1)
print(final_solar)

#merge
final_merged_data = pd.merge(final_solar, final_wind, on=['day'])
final_dataframe = final_merged_data.drop(['date_x', 'cloud_x', 'temp_x', 'rainfall_x', 'windspeed_x', 'Capacity_filled_y', 'Capacity_filled_x','direction_x', 'solar_predictions_x', 'solar_predictions_y',
                                          'wind_predictions_x', 'wind_predictions_y'],axis=1)
final_data = final_dataframe.rename(columns = {'date_y': 'date', 'cloud_y': 'cloud', 'temp_y':'temp', 'rainfall_y':'rainfall', 'windspeed_y':'windspeed', 'direction_y': 'direction',
                                               }, inplace = False)

#calculate the total output that will be used to measure less that 4.0 MW
final_data['Total_Output(MW)'] = final_data['Corrected_SolarFarm_Output'] + final_data['Corrected_WindFarm_Output']


# rearrange the columns and print the final dataframe
columns = ['day', 'date', 'cloud', 'temp', 'rainfall', 'windspeed', 'direction','Corrected_SolarFarm_Output','Corrected_WindFarm_Output', 'Total_Output(MW)']
final_dataframe = final_data[columns]
print(final_dataframe)



