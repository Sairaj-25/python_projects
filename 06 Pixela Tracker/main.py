import requests
from datetime import datetime
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
import os

# Load environment variables
load_dotenv()

TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token" : TOKEN,
    "username" : USERNAME,
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)

# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": "vscode1",
    "name": "VS Code Daily Usage",
    "unit": "hours",
    "type": "float",
    "color": "ajisai"  # purple (like GitHub green alternative)
}

headers = {
    "X-USER-TOKEN": TOKEN
}

response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
print(response.text)