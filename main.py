from data_manager import DataManager
from flight_search import FlightSearch

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()

# print(data_manager.get_data_rows())

data_manager.add_data_row(city="Boston", lowest_price=2000)

# example
data_manager = DataManager()

flight_search = FlightSearch()
flight_search.search_cheap_flights_for_rows(data_manager.get_data_rows())