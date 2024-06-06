import json

import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# load sheety api variables
load_dotenv(".env")
API_KEY = os.getenv("amadeus_api_key")
API_SECRET = os.getenv("amadeus_api_secret")

ENDPOINT = "https://test.api.amadeus.com"
ACCESS_TOKEN_URL = f"{ENDPOINT}/v1/security/oauth2/token"
AIRPORT_CITY_SEARCH_URL = f"{ENDPOINT}/v1/reference-data/locations"

FLIGHT_OFFERS_URL = f"{ENDPOINT}/v2/shopping/flight-offers"


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

        try:
            return response.json()['data'][0]['iataCode']
        except IndexError:
            print(f"{city_name} did not return any results from Airport search.")

    def search_cheap_flights(self, origin_city_code="LON", destination_city_code="NYC", time_window_days=180,
                             currency="EUR"):

        # Defining the time window to search
        today = datetime.now().today()
        end_date = today + timedelta(days=time_window_days)

        today = today.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": today,
            "returnDate": end_date,
            "adults": 1,
            "nonStop": "true",
            "currencyCode": currency,
            "max": "10",
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(FLIGHT_OFFERS_URL, headers=headers, params=query)
        response.raise_for_status()

        return response.json()


# example
flight_search = FlightSearch()
flight_search.search_cheap_flights()

# TODO: Use the Flight Search API to check for the cheapest flights from tomorrow to 6 months later for all the
#  cities in the Google Sheet.

# TODO: If the price is lower than the lowest price listed in the Google
#  Sheet then send an SMS (or WhatsApp Message) to your own number using the Twilio API.

# TODO: The SMS should include the departure airport IATA code,
#  destination airport IATA code, flight price and flight dates. e.g.
