import requests

# Hide API KEY
import os
from dotenv import load_dotenv
load_dotenv()


endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv("API_KEY")



weather_params = {
    "lat": 18.520430,
    "lon": 73.856743,
    "appid": api_key,
    "units": "metric"
}

response = requests.get(endpoint, params = weather_params)

"""

# Print the status code of the response
print(f"Status Code: {response.status_code}")

# Print the JSON content if the request was successful
if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.text)
    
"""

will_rain = False

data = response.json()

location = data["city"] ["name"]

for item in data["list"][:1]:  #[:1] first entry so next 3 hours and [:8] → 3x8=24 next 24 hours
    condition_id = item["weather"][0]["id"]
    if condition_id < 700:
        will_rain = True

if will_rain:
    print(f"📍 Location: {location}")
    print("☔ Rain expected in next 3 hours.")
else:
    print(f"📍 Location: {location}")
    print("🌤 No rain expected in next 3 hours.")




# This loop checks weather for the next 24 hours only. [:8] → 3x8=24 next 24 hours
"""

for item in response.json()["list"][:8]:
    print(item["dt_txt"], "-", item["weather"][0]["description"])

"""






