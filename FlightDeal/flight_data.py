
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, from_city: str, to_city: str, flight_data: list) -> None:
        self.get_important_flight_data(flight_data)
        self.from_city = from_city
        self.to_city = to_city
        self.google_booking_link = f"https://www.google.com/flights"
        
    
    def get_important_flight_data(self, flight_data: list):
        flight_data: dict = flight_data[0]
        self.departure_from = flight_data["flyFrom"]
        self.arrival_to = flight_data["flyTo"]
        
        self.flight_price = flight_data["price"]
        self.kiwi_booking_link = flight_data["deep_link"]
        self.local_departure_date = flight_data["local_departure"][ :flight_data["local_departure"].index("T")]
        self.local_return_date = flight_data["route"][-1]["local_arrival"][ :flight_data["route"][-1]["local_arrival"].index("T")]