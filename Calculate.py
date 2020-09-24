import pandas as pd
import numpy as np
from flask import Flask
from Predictions import df_predictions

#read in the maintenance csvs
wind_maintenance = pd.read_csv(r"C:\Users\Admin\Documents\AIIP\AppDev\Summative\wind_farm.csv")
solar_maintenance = pd.read_csv(r"C:\Users\Admin\Documents\AIIP\AppDev\Summative\solar_farm.csv")

#check the columns
print(wind_maintenance.columns)
print(solar_maintenance.columns)

# Rename the columns of both dataframe
wind_maintenance_2 = wind_maintenance.rename(columns={'Date Of Month': 'day', 'Capacity Available': 'Capacity'},
                                             inplace=False)
solar_maintenance_2 = solar_maintenance.rename(columns={'Date Of Month': 'day', 'Capacity Available': 'Capacity'},
                                               inplace=False)

# merge the dataframes to work on the adjusted wind output
new_wind = pd.merge(df_predictions, wind_maintenance_2, on=['day'])
new_wind['Predicted_WindFarm_Output(MW)'] = new_wind['wind_predictions'] * new_wind['Capacity'] / 100
final_wind = pd.merge(df_predictions, new_wind, how='outer', on='day', suffixes=('_', ''))
final_wind_data = final_wind.drop(['Capacity'], axis=1)
new_cols = final_wind_data.columns[final_wind_data.columns.str.endswith('_')]

#remove last char from column names
orig_cols = new_cols.str[:-1]
#dictionary for rename
d = dict(zip(new_cols, orig_cols))

#filter columns and replace NaNs by new appended columns
final_wind_data[orig_cols] = final_wind_data[orig_cols].combine_first(final_wind_data[new_cols].rename(columns=d))
#remove appended columns
final_wind_data = final_wind_data.drop(new_cols, axis=1)
wind_data = final_wind_data.replace(np.nan,0)
print(wind_data)
#final_wind_data.to_csv("corrected_wind_data.csv")

# merge the dataframes to work on the adjusted solar output
new_solar = pd.merge(df_predictions, solar_maintenance_2, on=['day'])
new_solar['Predicted_SolarFarm_Output(MW)'] = new_solar['solar_predictions'] * new_solar['Capacity'] / 100
final_solar = pd.merge(df_predictions, new_solar, how='outer', on='day', suffixes=('_', ''))
final_solar_data = final_solar.drop(['Capacity'], axis=1)
new_cols = final_solar_data.columns[final_solar_data.columns.str.endswith('_')]

#remove last char from column names
orig_cols = new_cols.str[:-1]
#dictionary for rename
d = dict(zip(new_cols, orig_cols))

#filter columns and replace NaNs by new appended columns
final_solar_data[orig_cols] = final_solar_data[orig_cols].combine_first(final_solar_data[new_cols].rename(columns=d))
#remove appended columns
final_solar_data = final_solar_data.drop(new_cols, axis=1)
solar_data = final_solar_data.replace(np.nan,0)
print(solar_data)

### MERGE BOTH TO ONE DF
solar_power = solar_data['Predicted_SolarFarm_Output(MW)']
wind_data["Predicted_SolarFarm_Output(MW)"] = solar_power
final_dataframe = wind_data
print(final_dataframe)