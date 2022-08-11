# ----------------- MODULES ----------------- #
import requests
import os
from datetime import datetime, timedelta

# ----------------- CONSTANTS ----------------- #
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "__________"
TOMMORROW_DATE = (datetime.now() + timedelta(1)).strftime("%d/%m/%Y")
IN_6_MONTHS_DATE = (datetime.now() + timedelta(180)).strftime("%d/%m/%Y")

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self) -> None:
        self.request_headers = {
            "apikey": TEQUILA_API_KEY,
        }
        
    def query(self, location: str, location_type: str = "city"):
        location_info = {
            "term": location,
            "location_types": location_type,
        }
        
        response = requests.get(url = f"{TEQUILA_ENDPOINT}/locations/query", params= location_info, headers= self.request_headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_IATA(self, location: str, location_type: str = "city"):
        data_received = self.query(location, location_type)
        IATA_code = data_received["locations"][0]["code"]
        return IATA_code
    
    def search_flights(self, from_city_code: str, to_city_code: str, max_price: int = 0, min_nights_of_stay: int = 0, max_nights_of_stay: int = 0, max_stopovers: int = 0, from_date: str = TOMMORROW_DATE, to_date: str = IN_6_MONTHS_DATE):
        flight_data = {
            "fly_from": from_city_code,
            "fly_to": to_city_code,
            "date_from": from_date,
            "date_to": to_date,
            "one_for_city": 1,
            "flight_type": "round",
            "max_stopovers": max_stopovers,
        }
        
        if (min_nights_of_stay > 0):
            flight_data.update({"nights_in_dst_from": min_nights_of_stay})
            
        if (max_nights_of_stay > 0):
            flight_data.update({"nights_in_dst_to": max_nights_of_stay})
        
        if (max_price > 0):
            flight_data.update({"price_to": max_price})
        
        response = requests.get(url = f"{TEQUILA_ENDPOINT}/v2/search", headers= self.request_headers, params = flight_data)
        response.raise_for_status()
        
        return response.json()["data"]