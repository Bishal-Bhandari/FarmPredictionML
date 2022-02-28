import requests, json

url = "https://api.openweathermap.org/data/2.5/weather?"
try:
    address = str(input("Enter the city name: "))
except ValueError:
    print("Given input is not valid.")
key = "39f081a68ade00a3fc22b0dbb10487cc"  # API key
final_url = url + "q=" + address + "&appid=" + key

response = requests.get(final_url)  # Sending HTTP request
if response.status_code == 200:

    # retrieving data in the json format
    data = response.json()

    # take the main dict block
    main = data['main']

    # getting temperature
    temperature = main['temp']
    # getting feel like
    temp_feel_like = main['feels_like']
    # getting the humidity
    humidity = main['humidity']
    # getting the pressure
    pressure = main['pressure']

    # weather report
    weather_report = data['weather']
    # wind report
    wind_report = data['wind']

    print(f"{address:-^35}")
    print(f"City ID: {data['id']}")
    print(f"Temperature: {temperature}")
    print(f"Feel Like: {temp_feel_like}")
    print(f"Humidity: {humidity}")
    print(f"Pressure: {pressure}")
    print(f"Weather Report: {weather_report[0]['description']}")
    print(f"Wind Speed: {wind_report['speed']}")
    print(f"Time Zone: {data['timezone']}")
else:
    print("Error in the connection.")
