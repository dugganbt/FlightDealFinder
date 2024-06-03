import requests
from dotenv import load_dotenv
import os

# load sheety api variables
load_dotenv(".env")
API_KEY = os.getenv("amadeus_api_key")
API_SECRET = os.getenv("amadeus_api_secret")

ENDPOINT = "https://test.api.amadeus.com/v1/"
ACCESS_TOKEN_URL = f"{ENDPOINT}security/oauth2/token"
AIRPORT_CITY_SEARCH_URL = f"{ENDPOINT}reference-data/locations"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self, api_key=API_KEY, api_secret=API_SECRET, access_token_url=ACCESS_TOKEN_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = self.get_access_token(access_token_url)

    def get_access_token(self, access_token_url):
        # Access token is needed to make requests to amadeus API
        # The token expires after 30 minutes

        response = requests.post(
            url=access_token_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.api_secret
            }
        )
        response.raise_for_status()
        return response.json()['access_token']

    def search_iata_code_for_city(self, city_name):
        global AIRPORT_CITY_SEARCH_URL
        # Given a city name return the IATA code of the closest major airport

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "keyword": city_name,
            "subType": "CITY"
        }
        response = requests.get(AIRPORT_CITY_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()['data'][0]['iataCode']

