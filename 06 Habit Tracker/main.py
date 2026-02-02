import requests
from datetime import datetime

Token = "samsndi0453jedi"
UserName = "sairaj0"
Graph_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": Token,
    "username": UserName,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{UserName}/graphs"

graph_config = {
    "id": Graph_ID,
    "name": "Cycling Graph",
    "unit": "km",
    "type": "float",
    "color": "ajisai"
}

# for Security api Key is provided in headers

headers = {
    "X-USER-TOKEN": Token
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
#
# print(response.text)

pixel_creation_endpoint = f"{pixela_endpoint}/{UserName}/graphs/{Graph_ID}"

# today = datetime.now() # 2024-09-26 16:46:39.250589

today = datetime(year=2024, month=9, day=25)
print(today.strftime("%Y%m%d")) # 20240926 --> using strftime() Method

pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "9.54",
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)

print(response.text)