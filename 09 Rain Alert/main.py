import requests

endpoint = "https://api.openweathermap.org/data/2.5/forecast"


api_key = "a89585a8397adf45e9ce756d32ce84be"

weather_params = {
    "lat": 18.520430,
    "lon": 73.856743,
    "appid": api_key
}

response = requests.get(endpoint, params = weather_params)

# Print the status code of the response
print(f"Status Code: {response.status_code}")

# Print the JSON content if the request was successful
if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.text)