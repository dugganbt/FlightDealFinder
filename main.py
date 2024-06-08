from data_manager import DataManager
from flight_search import FlightSearch

"""
This is a capstone project from the 100 days of Python code course by Angela Yu. 
"""

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()


# example
# add a new destination
data_manager.add_data_row(city="Boston", lowest_price=2000)

# Perform a flight search
flight_search = FlightSearch()
flight_search.search_cheap_flights_for_rows(data_manager.get_data_rows())