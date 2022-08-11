# ----------------- MODULES ----------------- #
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

# ----------------- CONSTANTS ----------------- #
PROJECT_NAME = "flightDeals"
PRICES_SHEET_NAME = "prices"
USERS_SHEET_NAME = "users"

CITY_FROM = "Cairo"
DEPARTURE_CITY_IATA_CODE = "CAI"

MIN_NIGHTS_OF_STAY = 7
MAX_NIGHTS_OF_STAY = 28

# ----------------- MAIN ----------------- #
prices_sheet_manager = DataManager(PROJECT_NAME, PRICES_SHEET_NAME)
flight_search = FlightSearch()

# PUT IATA CODE IN EACH CITY ROW
# Got current data from the sheet
current_data = prices_sheet_manager.retrieve_sheet_data()
rows_updated = False
# Looping through each row's data
for row in current_data[PRICES_SHEET_NAME]:
    if row["iataCode"] == "":
        # Determined row number
        row_num = current_data[PRICES_SHEET_NAME].index(row) + 2
        # Got the city name in the row
        city = row["city"]
        # Got that cit IATA code
        city_iata_code = flight_search.get_IATA(city)
        # Updated the row with it
        prices_sheet_manager.update_row("iataCode", city_iata_code, row_num)
        rows_updated = True

# Check if there are flights with a good deal
flights_found = []
if(rows_updated):
    sheet_rows: list = prices_sheet_manager.retrieve_sheet_data()[PRICES_SHEET_NAME]  # Retrieve the data of the cities I want to visit
else:
    sheet_rows: list = current_data[PRICES_SHEET_NAME]
    
for row in sheet_rows:  # Loop through each city
    # Get the required data of the city.
    to_city = row["city"]
    to_city_code = row["iataCode"]
    try:
        max_price = int(row["averagePrice"])
    except:
        max_price = 0
    
    # Check for flights for that city with 0 or 1 stopovers
    flight_data = flight_search.search_flights(DEPARTURE_CITY_IATA_CODE, to_city_code, max_price, MIN_NIGHTS_OF_STAY, MAX_NIGHTS_OF_STAY, 1)
    
    # If a flight was found
    if (len(flight_data) != 0 and flight_data[0]["availability"]["seats"] != None):
        flight = FlightData(CITY_FROM, to_city, flight_data)    # Create a Flightdata class out of the flight data
        flights_found.append(flight)    # Add it to flights found.
         
# If low price flights was found 
if(len(flights_found) != 0):
    emails_sheet_manager = DataManager(PROJECT_NAME, USERS_SHEET_NAME)
    users_data = emails_sheet_manager.retrieve_sheet_data()[USERS_SHEET_NAME]
    # Send a message with the flight details for each flight found
    notfication_manager = NotificationManager()
    for flight in flights_found:
        msg = f"Low price alert! Only €{flight.flight_price} to fly from {flight.from_city}-{flight.departure_from} to {flight.to_city}-{flight.arrival_to}, from {flight.local_departure_date} to {flight.local_return_date}\nKiwi Booking Link:\n{flight.kiwi_booking_link}\nYou can check for the flight on google manually:\n{flight.google_booking_link}"
        notfication_manager.send_message(msg)
        
        email_msg = f"Subject: Good Flight deal to {flight.to_city}\n\n" + msg
        email_msg = email_msg.encode('utf-8')
        for user in users_data:
            user_email = user["email"]
            notfication_manager.send_email(user_email, email_msg)
            
    notfication_manager.connection.close()