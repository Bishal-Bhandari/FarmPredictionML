import requests
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import date
from openpyxl import load_workbook

url = "https://api.openweathermap.org/data/2.5/weather?"
try:
    address = 'Kathmandu'  # str(input("Enter the city name: "))
except ValueError:
    print("Given input is not valid.")
key = "key"  # API key
final_url = url + "q=" + address + "&appid=" + key

response = requests.get(final_url)  # Sending HTTP request
if response.status_code == 200:

    Req_Data_Inner = []
    Req_Data_Main = []
    Day_Feature = []
    # retrieving data in the json format
    data = response.json()
    # take the main dict block
    main = data['main']
    # converting kelvin temp to Celsius
    Temp_Kelvin = main['temp']
    Temp_Cel = int(Temp_Kelvin - 273.15)
    # wind report
    wind_report = data['wind']
    # For current date
    today = date.today()
    # For making list of list for weather data
    for j in range(0, 1):
        for i in range(0, 1):
            Req_Data_Inner.clear()
            Req_Data_Inner.append(address)
            Req_Data_Inner.append(today.year)
            Req_Data_Inner.append(today.day)
            Req_Data_Inner.append(today.month)
            Req_Data_Inner.append(Temp_Cel)
            Req_Data_Inner.append(main['humidity'])
            Req_Data_Inner.append(wind_report['speed'])
            # for the condition of day
            if Temp_Cel > 10:
                Day_Feature.append("Cold")
                if main['humidity'] <= 20:
                    Day_Feature.append("Low Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
                elif 21 <= main['humidity'] <= 60:
                    Day_Feature.append("Mild Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
                elif 61 <= main['humidity'] <= 100:
                    Day_Feature.append("Ok Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
            elif 10 >= Temp_Cel >= 20:
                Day_Feature.append("Warm")
                if main['humidity'] <= 20:
                    Day_Feature.append("Low Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
                elif 21 <= main['humidity'] <= 60:
                    Day_Feature.append("Mild Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
                elif 61 <= main['humidity'] <= 100:
                    Day_Feature.append("Ok Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
            elif 21 >= Temp_Cel >= 30:
                Day_Feature.append("Hot")
                if main['humidity'] <= 20:
                    Day_Feature.append("Low Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
                elif 21 <= main['humidity'] <= 60:
                    Day_Feature.append("Mild Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
                elif 61 <= main['humidity'] <= 100:
                    Day_Feature.append("Ok Humidity")
                    if wind_report['speed'] <= 10:
                        Day_Feature.append("Low Wind")
                    elif 11 <= wind_report['speed'] <= 20:
                        Day_Feature.append("Mild Wind")
                    else:
                        Day_Feature.append("High Wind")
            else:
                Day_Feature = "Not Suitable"
            Req_Data_Inner.append(str(Day_Feature))  # appending the day feature
            Req_Data_Main.append(Req_Data_Inner)  # appending the inner list to main list
            break
else:
    print("Error in the connection.")

# using excel file to save data
Sheet_Name = 'Weatherdata.xlsx'
Data_File = load_workbook(Sheet_Name)
page = Data_File.active
# New data to write
for info in Req_Data_Main:
    page.append(info)
Data_File.save(filename=Sheet_Name)
# read file
Read_File = pd.read_excel(r'Weatherdata.xlsx')

# ML to predict
Input_Dataset_Init = Read_File.drop(columns=['City'])
Input_Dataset = Input_Dataset_Init.drop(columns=['Condition'])
Output_Dataset = Read_File['Condition']
# using tree
Mod_Tree = DecisionTreeClassifier()
Mod_Tree.fit(Input_Dataset.values, Output_Dataset)
Prediction_Result = Mod_Tree.predict([[2022, 2, 3, 21, 5, 5]])
# prediction based on previous data
print(f"The result after prediction is as below:\n {Prediction_Result}")
