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
    for j in range(0, 2):
        for i in range(0, 2):
            Req_Data_Inner.clear()
            Req_Data_Inner.append(address)
            Req_Data_Inner.append(today.year)
            Req_Data_Inner.append(today.day)
            Req_Data_Inner.append(today.month)
            Req_Data_Inner.append(Temp_Cel)
            Req_Data_Inner.append(main['humidity'])
            Req_Data_Inner.append(wind_report['speed'])
            Req_Data_Main.append(Req_Data_Inner)  # appending the inner list to main list
            break
    Req_Data_Main = Req_Data_Main
    print(f"main req dataa {Req_Data_Main}")

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
x = Read_File.drop(columns=['City'])
y = Read_File['City']
x_train, x_test, y_train, y_test = train_test_split(x.values, y.values, test_size=0.0001)

model = DecisionTreeClassifier()
model.fit(x.values, y.values)
pred = model.predict(x_test)
score = accuracy_score(y_test, pred)
print(score)
