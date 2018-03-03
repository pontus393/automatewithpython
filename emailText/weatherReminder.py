#! python3
# Checks weather in given city and texts you the weather
# Schedule in Windows Task Scheduler

import json, requests
from twilio.rest import Client

def sendMessage(message):
    accountSID = '<INSERT TWILIO ACCOUNT SID>'
    authToken = '<INSERT TWILIO AUTH TOKEN>'
    client = Client(accountSID, authToken)

    message = client.messages.create(
    to="<INSERT RECEIVER TELEPHONE NO>",
    from_="<INSERT TWILIO TELEPHONE NO>",
    body=message)

    print("Done!")

# Downloading weather data from Open Weather Map
city = '<INSERT CITY>'
appId = '<INSERT APP ID FROM OPENWEATHERMAP>'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(city, appId)

response = requests.get(url)
response.raise_for_status()

# Load weather data into Python variable

weatherData = json.loads(response.text)

currentWeather = weatherData['weather'][0]['main'] # t.ex. "clear"
currentTemp = round(weatherData['main']['temp'] - 273, 0) # t.ex. "-1.22"

# Send warnings either if it's raining or freezing

sendMessage("Today's weather in {} will be {} and the temperature will be {}".format(city, currentWeather, currentTemp))
