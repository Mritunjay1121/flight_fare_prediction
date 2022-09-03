import os
import sys

from housing.exception import FlightfareException
from housing.util.util import load_object

import pandas as pd


class FlightFareData:

    def __init__(self,
                 Airline: str,
                 Source: str,
                 Destination: str,
                 Total_Stops: float,
                 Journey_day: float,
                 Journey_month: float,
                 Dep_hour: float,
                 Dep_min: float,
                 Arrival_hour: float,
                 Arrival_min: float,
                 Duration_hours: float,
                 Duration_mins: float,
                 Price: float = None
                ):


                
                
        try:
            self.Airline = Airline
            self.Source = Source
            self.Destination = Destination
            self.Total_Stops = Total_Stops
            self.Journey_day = Journey_day
            self.Journey_month = Journey_month
            self.Dep_hour = Dep_hour
            self.Dep_min = Dep_min
            self.Arrival_hour = Arrival_hour
            self.Arrival_min = Arrival_min
            self.Duration_hours = Duration_hours
            self.Duration_mins = Duration_mins
            self.Price = Price
        except Exception as e:
            raise FlightfareException(e, sys) from e

    def get_housing_input_data_frame(self):

        try:
            housing_input_dict = self.get_housing_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise FlightfareException(e, sys) from e

    def get_housing_data_as_dict(self):
        try:
            input_data = {
                "Airline": [self.Airline],
                "Source": [self.Source],
                "Destination": [self.Destination],
                "Total_Stops": [self.Total_Stops],
                "Journey_day": [self.Journey_day],
                "Journey_month": [self.Journey_month],
                "Dep_hour": [self.Dep_hour],
                "Dep_min": [self.Dep_min],
                "Arrival_hour": [self.Arrival_hour],
                "Arrival_min": [self.Arrival_min],
                "Duration_hours": [self.Duration_hours],
                "Duration_mins": [self.Duration_mins]}
            return input_data
        except Exception as e:
            raise FlightfareException(e, sys)


class FlighFarePredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise FlightfareException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise FlightfareException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise FlightfareException(e, sys) from e


# import os
# import sys

# from housing.exception import FlightfareException
# from housing.util.util import load_object

# import pandas as pd


# class FlightFareData:

#     def __init__(self,
#                  Total_Stops: float,
#                  Journey_day: float,
#                  Journey_month: float,
#                  Dep_hour: float,
#                  Dep_min: float,
#                  Arrival_hour: float,
#                  Arrival_min: float,
#                  Duration_hours: float,
#                  Duration_mins: float,
#                  median_house_value: float = None
#                  ):
#         try:
#             self.longitude = longitude
#             self.latitude = latitude
#             self.housing_median_age = housing_median_age
#             self.total_rooms = total_rooms
#             self.total_bedrooms = total_bedrooms
#             self.population = population
#             self.households = households
#             self.median_income = median_income
#             self.ocean_proximity = ocean_proximity
#             self.median_house_value = median_house_value
#         except Exception as e:
#             raise FlightfareException(e, sys) from e

#     def get_housing_input_data_frame(self):

#         try:
#             housing_input_dict = self.get_housing_data_as_dict()
#             return pd.DataFrame(housing_input_dict)
#         except Exception as e:
#             raise FlightfareException(e, sys) from e

#     def get_housing_data_as_dict(self):
#         try:
#             input_data = {
#                 "longitude": [self.longitude],
#                 "latitude": [self.latitude],
#                 "housing_median_age": [self.housing_median_age],
#                 "total_rooms": [self.total_rooms],
#                 "total_bedrooms": [self.total_bedrooms],
#                 "population": [self.population],
#                 "households": [self.households],
#                 "median_income": [self.median_income],
#                 "ocean_proximity": [self.ocean_proximity]}
#             return input_data
#         except Exception as e:
#             raise FlightfareException(e, sys)


# class FlighFarePredictor:

#     def __init__(self, model_dir: str):
#         try:
#             self.model_dir = model_dir
#         except Exception as e:
#             raise FlightfareException(e, sys) from e

#     def get_latest_model_path(self):
#         try:
#             folder_name = list(map(int, os.listdir(self.model_dir)))
#             latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
#             file_name = os.listdir(latest_model_dir)[0]
#             latest_model_path = os.path.join(latest_model_dir, file_name)
#             return latest_model_path
#         except Exception as e:
#             raise FlightfareException(e, sys) from e

#     def predict(self, X):
#         try:
#             model_path = self.get_latest_model_path()
#             model = load_object(file_path=model_path)
#             median_house_value = model.predict(X)
#             return median_house_value
#         except Exception as e:
#             raise FlightfareException(e, sys) from e