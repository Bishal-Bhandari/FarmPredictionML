import datetime

import requests
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from datetime import date
from openpyxl import load_workbook


def URL_Data():
    url = "https://api.openweathermap.org/data/2.5/weather?"
    try:
        address = 'Kathmandu'  # str(input("Enter the city name: "))
    except ValueError:
        print("Given input is not valid.")
    key = "39f081a68ade00a3fc22b0dbb10487cc"  # API key
    final_url = url + "q=" + address + "&appid=" + key
    response = requests.get(final_url)  # Sending HTTP request
    List_Data(response, address)


def List_Data(response, address):
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
        Temp_Cel = round((Temp_Kelvin - 273.15), 2)
        print(Temp_Cel)
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
    File_Work(Req_Data_Main)


def File_Work(Req_Data_Main):
    # using excel file to save data
    Sheet_Name = 'Weatherdata.xlsx'
    Data_File = load_workbook(Sheet_Name)
    page = Data_File.active
    # New data to write
    for info in Req_Data_Main:
        page.append(info)
    Data_File.save(filename=Sheet_Name)


def DescisionTree():
    # read file
    Read_File = pd.read_excel(r'Weatherdata.xlsx')

    # ML to predict
    Input_Dataset_Cond1 = Read_File.drop(columns=['City', 'Year', 'Temp', 'Humidity', 'WindSpeed', 'Condition'])
    Input_Dataset_Cond2 = Read_File.drop(columns=['City', 'Condition'])
    Output_Dataset = Read_File['Condition']
    # using tree
    Mod_Tree = DecisionTreeClassifier()

    choice = input("Press '1' for prediction based on previous data. Press '2' for prediction based on user given "
                   "data:  ")
    if int(choice) == 1:
        # taking the input from user
        date_user_day, date_user_month = input("\nEnter day and month (Format: DD-MM): ").split("-")
        # form above for prediction using tree
        Mod_Tree.fit(Input_Dataset_Cond1.values, Output_Dataset)
        # prediction with given data
        Prediction_Result = Mod_Tree.predict([[date_user_day, date_user_month]])
        # prediction based on previous data
        print(f"The result after prediction is as below:\n {Prediction_Result[0]}")
    elif int(choice) == 2:
        # taking the input from user
        print("\nEnter the data for the prediction.")
        date_user = input('Enter the date (DD-MM-YYYY): ')
        try:
            date_user = datetime.datetime.strptime(date_user, "%d-%m-%Y")
        except ValueError:
            print("Error: must be format dd-mm-yyyy ")
        temp_user = int(input("Enter the temperature: "))
        humidity_user = int(input("Enter the humidity: "))
        wind_user = int(input("Enter the wind speed: "))
        # form above for prediction using tree
        Mod_Tree.fit(Input_Dataset_Cond2.values, Output_Dataset)
        # prediction with given data
        Prediction_Result = Mod_Tree.predict([[date_user.year, date_user.day, date_user.month, temp_user, humidity_user,wind_user]])
        # prediction based on previous data
        print(f"The result after prediction is as below:\n {Prediction_Result[0]}")
    else:
        print("Please enter proper value.")


URL_Data()
DescisionTree()
