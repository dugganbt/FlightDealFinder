import requests
from dotenv import load_dotenv
import os
from datetime import datetime

# load sheety api variables
load_dotenv(".env")
USERNAME = os.getenv("sheety_user")
PROJECT_NAME = os.getenv("sheety_projectname")
SHEET_NAME = os.getenv("sheety_sheetname")
TOKEN = os.getenv("sheety_token")

ENDPOINT = f"https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEET_NAME}"


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self, username=USERNAME, project_name=PROJECT_NAME, sheet_name=SHEET_NAME, token=TOKEN,
                 endpoint=ENDPOINT):
        self.username = username
        self.project_name = project_name
        self.sheet_name = SHEET_NAME
        self.headers = {f"Authorization": f"Bearer {TOKEN}"}
        self.endpoint = endpoint


    def get_data_rows(self):
        return requests.get(url=self.endpoint, headers=self.headers).json()

    def add_data_row(self, city, iata_code, lowest_price):
        data = {
            "price":{
                "city": city.title(),
                "iataCode": iata_code.title(),
                "lowestPrice": lowest_price
            }
        }

        # put the data in the sheet
        response = requests.post(
            url=self.endpoint,
            json=data,
            headers=self.headers
        )

        response.raise_for_status()


    def add_iata_code_for_city(self):
        pass