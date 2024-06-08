import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

from flight_data import FlightData
from notification_manager import NotificationManager


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
        """    Access token is needed to make requests to amadeus API
            the token expires after 30 minutes"""

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
        """Given a city name return the IATA code of the closest major airport."""

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

    def search_cheap_flight(self, origin_city_code="LON", destination_city_code="NYC", time_window_days=180,
                             currency="EUR"):

        """Search the cheapest flight for a single connection. Return a FlightData object if connection found,
        returns 'N/A', if no connection found."""

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

        # Assuming the first flight returned is the cheapest
        try:
            cheapest_flight = FlightData(response.json()['data'][0])
        except IndexError:
            print(f"No data returned for flights from {origin_city_code} to {destination_city_code}")
            cheapest_flight = "N/A"
        except KeyError:
            print(f"No data returned for flights from {origin_city_code} to {destination_city_code}")
            cheapest_flight = "N/A"

        return cheapest_flight

    def search_cheap_flights_for_rows(self, destinations_to_check):
        """Given a list of destinations, iata codes and prices from the data_manager it searches for the cheapest
        connection. Prints the results"""

        for destination in destinations_to_check:
            cheapest_connection = self.search_cheap_flight(destination_city_code=destination["iataCode"])
            if cheapest_connection != "N/A":
                print(f"Destination: {destination["city"]}, desired price: {destination["lowestPrice"]}, available "
                      f"price: {cheapest_connection.price}")

                if float(cheapest_connection.price) <= float(destination["lowestPrice"]):
                    print("Notification sent!")
                    notifier = NotificationManager()
                    message = (
                        f"Low price alert! "
                        f"Only {cheapest_connection.price} to fly from {cheapest_connection.outbound_departure_airport.strip()} "
                        f"to {cheapest_connection.outbound_arrival_airport.strip()} "
                        f"on {cheapest_connection.outbound_departure_datetime}. "
                        f"Return flight from {cheapest_connection.return_departure_airport.strip()} "
                        f"on {cheapest_connection.return_departure_datetime}."
                    )
                    notifier.send_notification_whatsapp(message_text=message)