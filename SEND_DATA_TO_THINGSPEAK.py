#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os.path
import gspread
import json
from google.oauth2.service_account import Credentials
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Assume 'json_content' is a string containing your JSON data.
json_content = """
{
  "type": "service_account",
  "project_id": "project-wether-station-389011",
  "private_key_id": "7bcb60c652069eca5a0e9f059c229c8d489910f7",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDKz5gM2XwdZyHu\\nAx4GDJAQUOa1H7xm7rBq9Vhvhjp9DuQyVnQtbDHAPw13EthhXNGqmeBujvxt/e50\\nYiKsc80i7gRhXaiiRetg95F/rKkQqOLiVlHcquNd1kkH0jQWhR0N3wcFRlw8AIsg\\nhBNKQs6a4KHIYklxio4NZomipK6kppB778aFhBZr3o8iHijkSbd/FKTheL1rDfok\\n2J7Qc4fMUjXZbde8T52BEXtKECPQTJLaFoy2IIMlgbXwFit7A0wif0nYiIKBV/Bi\\nDgVHnONRyJKzeyiP/KE7LmvNNRaaA8p1/NwfhNo3Bqyy7eUltyLrVq9AAh1kZIO5\\nUXrGKGYJAgMBAAECggEADZFhiFOI630lrpMAEFLJFQRaiNm6jI7Rl9g5zj02Pr1P\\nLCRvQYYsVmKJe7KzreDMKIwCkRbpAZFEQX46uFuHaNuwSJS/1jpT/sDVN6vFBDeu\\nNQrmD1uR2ipeqKKqCCsn2FCYO0S7oSp+pEJduYE6ae9W921G4U0OB4y5brtycRKS\\niYfDv3wvA3gGjClmxLgiR7gqejhFwvzUDMKqi0UXKzgNQ+knQx7ihrp6StMvPTHd\\nkUF6Yd74DC/Zq31L0byxYpE6H7vXdOWD14bObdNAzA3K/hZHCD706cm4qpFxg12P\\n4lrFWCCg4pAbVg5fxhxzE87q2WV3IPWjGBuPg9qmwQKBgQDy1hTg5JBPix3bglCH\\nIMcv1T5S2K5cF2+HEOG4z/921LMTUDDek3rRNBSzqYWDCpMazjAzeiru3VkiojUY\\nz3MKi96BGL564bjKT1hP+5z8TfADIGvlw1HXHFW9pHx+GbW9TOTIRGmenn89jWdx\\nLBvWhr/SRWrINp6cTFialBbEQQKBgQDVzhFMqAsRIfxaP6lCb7SKUGj3yxK9cxXg\\nBQprTPjJ1qfFJu/93Z/s5azDdrx5WiTF3WefFXIbLlHooKA8UlRdGotnDyChtpW6\\nEpWYxB4NotlWzifUGXxtMcdODjS7zwB1o2GQNXcXw0yxeXZCjKlLIxlPXAn03Orx\\nBhEbfqiPyQKBgQDbTrIuZN1bqQT/AFKfpt+c+FW/1kapjtS/Q2THVrmdZPyRHaP0\\n73ZEx2dG1ntoXD18QOhRJSzu6mKcn6eaT4fS53y8VE96hK4xr7TPDyq4xd5TxI0N\\nRPd9cO6SRaHU9H0oh/A6WWaVxQie2zynfbFqbemBCgYk6QcXmu+OMt3YwQKBgFgS\\nDmY5QnXIPh8e4iYPxZrEDLkl2Y5YfcZNzUDt7/2Ugn9fzrQQOvRml4fcvT5vt34Z\\n+bk6KEqyBeOBZv/yGfZQHORTAuoaQArp5N2My6RqVITBXv6rkOmZ+7NXfrluR44t\\nwt6YZ3pOZKUml2RKdOISjzZ1f1RyPAUUrq9YuS6hAoGAHSjfgRojTXKQLeLPcAGC\\n57QNCGwjA5L6x8DhUalSFnPoMgZjjjgvkn2FYM7BPjl4gRSj/jt3qr7iF7dym7po\\npaHIDAvKy4vTYG0mJwflRKlL/rdSAS4Uqp2y8Ve/vWJjmqKSUGJZYyAP1xOfcORV\\nipbyfm/OPbBy9/zIPCNAoas=\\n-----END PRIVATE KEY-----\\n",
  "client_email": "weatherwisper@project-wether-station-389011.iam.gserviceaccount.com",
  "client_id": "101032223948604457948",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/weatherwisper%40project-wether-station-389011.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

json_key = json.loads(json_content)

# Use credentials to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_info(json_key, scopes=scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("WEATHER_STATION_MAIN_DATA_COLLECTOR").sheet1

# Extract all data into a DataFrame
data = sheet.get_all_records()
last_records = data[-15:]
# print(last_records)


# In[ ]:


raw_weather_df = pd.DataFrame(last_records)
print(raw_weather_df)


# In[ ]:


# Calculate averages
avg_temperature = raw_weather_df['TEMPERATURE'].mean()
avg_humidity = raw_weather_df['HUMIDITY'].mean()
avg_pressure = raw_weather_df['PRESSURE'].mean()
avg_lux = raw_weather_df['LUX'].mean()
avg_rain_fall = raw_weather_df['RAIN FALL'].mean()
avg_wind_speed = raw_weather_df['WIND SPEED'].mean()

# Calculate modes
rain_status_mode = raw_weather_df['RAINSTATUS'].mode()[0]
wind_direction_mode = raw_weather_df['WIND DIRECTION'].mode()[0]

# print('Average Temperature:', avg_temperature)
# print('Average Humidity:', avg_humidity)
# print('Average Pressure:', avg_pressure)
# print('Average Lux:', avg_lux)
# print('Average Rain Fall:', avg_rain_fall)
# print('Average Wind Speed:', avg_wind_speed)
# print('Mode of Rain Status:', rain_status_mode)
# print('Mode of Wind Direction:', wind_direction_mode)


# In[ ]:


import requests

# ThingSpeak settings
url = 'https://api.thingspeak.com/update'
api_key = 'RU5LKXZPEWUWQJM2'

data = {
    'api_key': api_key,
    'field1': avg_temperature,
    'field2': avg_humidity,
    'field3': avg_pressure,
    'field4': avg_lux,
    'field8': avg_rain_fall,
    'field5': avg_wind_speed,
    'field7': rain_status_mode,
    'field6': wind_direction_mode,
}

# Send the data
response = requests.post(url, params=data)

if response.status_code == 200:
    print('Data sent to ThingSpeak successfully')
else:
    print('Failed to send data to ThingSpeak')

