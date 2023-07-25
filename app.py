from flask import Flask, jsonify
import os.path
import gspread
import json
from google.oauth2.service_account import Credentials
import pandas as pd
from neuralprophet import NeuralProphet
import pickle

app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def get_forecast():
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
    last_records = data[-17280:]
    # print(last_records)
    
    # In[2]:
    
    raw_weather_df = pd.DataFrame(last_records)
    print(raw_weather_df)
    
    # In[3]:
    
    raw_weather_df.drop(raw_weather_df.columns[[6,7,9]],axis=1,inplace=True)
    preprocessed_weather_df = raw_weather_df
    print(preprocessed_weather_df)
    
    # In[4]:
    
    preprocessed_weather_df["datetime"] = pd.to_datetime(preprocessed_weather_df["DATE"]+' '+preprocessed_weather_df["TIME"])
    # print(preprocessed_weather_df)
    # preprocessed_weather_df = preprocessed_weather_df.set_index('datetime')
    preprocessed_weather_df = preprocessed_weather_df.drop(['DATE','TIME'],axis = 1)
    print(preprocessed_weather_df)
    
    # # check status of data
    
    pressure_data = preprocessed_weather_df[["datetime","PRESSURE"]]
    pressure_data.dropna(inplace=True)
    pressure_data['datetime'] = pd.to_datetime(pressure_data['datetime'])
    pressure_data.set_index('datetime', inplace=True)
    pressure_data = pressure_data.resample('5T').mean()
    pressure_data.reset_index(inplace=True)
    pressure_data.columns = ['ds','y']
    pressure_data['y'].fillna((pressure_data['y'].median()), inplace=True)
    pressure_data['y'] = pressure_data['y'] / 100.0
    pressure_data
    
    
    # # train the model
    
    # In[62]:
    
    
    model = NeuralProphet()
    
    model.fit(pressure_data, freq='5T')
    
    future = model.make_future_dataframe(pressure_data, periods=12)
    forecast = model.predict(future)
    
    
    # def zambretti(pressure, trend, is_northern_hemisphere=True):
    #     zambretti_dict = {
    #         'A': 'Settled fine', 'B': 'Fine weather', 'C': 'Becoming fine', 'D': 'Fairly fine, improving', 'E': 'Fairly fine, possible showers', 'F': 'Showery early, improving',
    #         'G': 'Changeable', 'H': 'Fairly fine, showers likely', 'I': 'Showery bright intervals', 'J': 'Showery, becoming less settled', 'K': 'Changeable, some rain',
    #         'L': 'Unsettled, short fine intervals', 'M': 'Unsettled, rain later', 'N': 'Unsettled, some rain', 'O': 'Very unsettled, rain', 'P': 'Stormy, much rain'
    #     }
        
    #     if is_northern_hemisphere:
    #         if trend < 0:  # falling
    #             value = int((1020 - pressure) * 0.033) + 65
    #         elif trend > 0:  # rising
    #             value = int((1050 - pressure) * 0.033) + 65
    #         else:  # steady
    #             value = int((1030 - pressure) * 0.033) + 65
    #     else:  # southern hemisphere
    #         if trend < 0:  # falling
    #             value = int((1050 - pressure) * 0.033) + 65
    #         elif trend > 0:  # rising
    #             value = int((1020 - pressure) * 0.033) + 65
    #         else:  # steady
    #             value = int((1030 - pressure) * 0.033) + 65
    
    #     # Check if value is within the valid range for chr()
    #     if 0 <= value <= 1_114_111:
    #         letter = chr(value)
    #     else:
    #         return 'Invalid prediction due to out of range pressure value'
    
    #     return zambretti_dict.get(letter, 'Invalid prediction')
    
    
    # # Do the Short Term Forecasting
    
    # In[65]:
    
    
    pressure_trend = forecast['trend'].values[-1]
    pressure_forecast = forecast['yhat1'].values[-1]
    is_northern_hemisphere = True
    # zambretti_forecast = zambretti(pressure_forecast, pressure_trend, is_northern_hemisphere)
    # print(zambretti_forecast)

    
    # ThingSpeak settings
      url = 'https://api.thingspeak.com/update'
      api_key = 'P5V9UF0WNJDHS3U0'
      
      data = {
          'api_key': api_key,
          'field1': pressure_trend,
          'field2': pressure_forecast
      }
      
      # Send the data
      response = requests.post(url, params=data)
    
      if response.status_code == 200:
          return 'Data sent to ThingSpeak successfully'
      else:
          return 'Failed to send data to ThingSpeak'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

