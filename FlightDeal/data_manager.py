# ----------------- MODULES ----------------- #
import requests
import os

# ----------------- CONSTANTS ----------------- #
SHEETY_ENDPOINT = "https://api.sheety.co"
# SHEETY_USERNAME = os.environ["SHEETY_USERNAME"]
# SHEETY_AUTH_KEY = os.environ["SHEETY_AUTH_KEY"]
SHEETY_USERNAME = "____________"
SHEETY_AUTH_KEY = "____________"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self, project_name: str, sheet_name: str) -> None:
        self.project_name = project_name
        self.sheet_name = sheet_name
        self.request_headers = {
            "Authorization": SHEETY_AUTH_KEY,
        }
        
        
    def retrieve_sheet_data(self) -> dict:
        response = requests.get(url = f"{SHEETY_ENDPOINT}/{SHEETY_USERNAME}/{self.project_name}/{self.sheet_name}", headers= self.request_headers)
        response.raise_for_status()
        
        data = response.json()
        
        return data
    
    def update_row(self, property_to_update: str, update_value: str, row_num: str):
        """Function that updates a row column.

        Args:
            property_to_update (str): The name of the column you want to update.
            update_value (str): The value you want to be inserted
            row_num (str): The no of row you want to update.
        """
        request_headers = {
            "Authorization": SHEETY_AUTH_KEY,
            "Content-Type": "application/json"
        }
        
        data_to_send = {
            self.sheet_name[:-1]: {
                property_to_update: update_value,
            },
        }
        
        response = requests.put(url = f"{SHEETY_ENDPOINT}/{SHEETY_USERNAME}/{self.project_name}/{self.sheet_name}/{str(row_num)}", json= data_to_send, headers= request_headers)
        response.raise_for_status()
        