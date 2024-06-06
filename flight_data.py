from datetime import datetime


class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self, a_flight_data_json):
        self.price = None

        self.outbound_departure_airport = None
        self.outbound_arrival_airport = None
        self.return_departure_airport = None
        self.return_arrival_airport = None

        self.outbound_departure_datetime = None
        self.outbound_arrival_datetime = None
        self.return_departure_datetime = None
        self.return_arrival_datetime = None

        self.outbound_airline_code = None
        self.return_airline_code = None

        self.extract_data(a_flight_data_json)

    def extract_data(self, data):
        # Extract and clean the price
        self.price = float(data['price']['grandTotal'].strip())

        # Extract outbound details
        outbound_segment = data['itineraries'][0]['segments'][0]
        self.outbound_departure_airport = outbound_segment['departure']['iataCode'].strip()
        self.outbound_arrival_airport = outbound_segment['arrival']['iataCode'].strip()

        self.outbound_departure_datetime = self.clean_datetime(outbound_segment['departure']['at'])
        self.outbound_arrival_datetime = self.clean_datetime(outbound_segment['arrival']['at'])

        self.outbound_airline_code = outbound_segment['carrierCode'].strip()

        # Extract return details
        return_segment = data['itineraries'][1]['segments'][0]
        self.return_departure_airport = return_segment['departure']['iataCode'].strip()
        self.return_arrival_airport = return_segment['arrival']['iataCode'].strip()

        self.return_departure_datetime = self.clean_datetime(return_segment['departure']['at'])
        self.return_arrival_datetime = self.clean_datetime(return_segment['arrival']['at'])

        self.return_airline_code = return_segment['carrierCode'].strip()

    def clean_datetime(self, datetime_str):
        cleaned_str = ''.join(datetime_str.split())
        return datetime.strptime(cleaned_str, '%Y-%m-%dT%H:%M:%S')
