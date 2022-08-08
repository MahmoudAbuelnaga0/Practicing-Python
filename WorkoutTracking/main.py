# ------------------ MODULES ------------------ #
import requests
import os
from datetime import datetime

# ------------------ CONSTANTS ------------------ #
# NutritioniX details
NUTRITIONIX_APP_ID = os.environ["NUTRITIONIX_APP_ID"]
NUTRITIONIX_API_KEY = os.environ["NUTRITIONIX_API_KEY"]
NUTRITIONIX_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
GENDER = "male"
WEIGHT_KG = 80.3
HEIGHT_CM = 180
AGE = 20

# Sheety details
SHEETY_ENDPOINT = "https://api.sheety.co"
SHEETY_AUTH_KEY = os.environ["SHEETY_AUTH_KEY"]
SHEETY_USERNAME = os.environ["SHEETY_USERNAME"]
PROJECT_NAME = "workoutTracking"
SHEET_NAME = "workouts"

# ------------------ FUNCTIONS ------------------ #
def exercise_calories(query: str, gender: str = GENDER, weight: float = WEIGHT_KG, height: float = HEIGHT_CM, age: int = AGE) -> list:
    """Function that get the calories burned for the exercises entered.
    The function to the following API: "https://trackapi.nutritionix.com/v2/natural/exercise" which depends on NLP and returns a json with the duration and calories burned for each entered exercise.

    Args:
        query (str): Query that describes the exercise you did and the duration of that exercise or the distance done (You just write the exercises in simple English language like "Ran for 3km and cycled for 5mins").
        gender (str, optional): "male" or "female". Defaults to GENDER.
        weight (float, optional): Weight in Kilograms. Defaults to WEIGHT_KG.
        height (float, optional): Height in Centimeters. Defaults to HEIGHT_CM.
        age (int, optional): Age in years. Defaults to AGE.

    Returns:
        list: list of dictonaries where each dictionary has an exercise information.
    """
    
    # Send post request to the NutritionX Endpoint and get calories burned from each exercise
    exercise_details = {
        "query": query, # A string that explains the exercise you did
        "gender": gender,
        "weight_kg": weight,
        "height_cm": height,
        "age": age,
    }
    
    request_headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "x-remote-user-id": "0",
    }
    
    response = requests.post(url = NUTRITIONIX_EXERCISE_ENDPOINT, data = exercise_details, headers= request_headers)
    response.raise_for_status()
    exercises_details = response.json()["exercises"]
    
    exercises = [{"exercise": exercise["name"],"duration": exercise["duration_min"], "calories": exercise["nf_calories"]}  for exercise in exercises_details]
    return exercises

def retrieve_sheet_data(project_name: str = PROJECT_NAME, sheet_name: str = SHEET_NAME) -> dict:
    """Function connects to the following API: "https://api.sheety.co" and retrieve data of specified sheet.

    Args:
        project_name (str, optional): Project name on Sheety (Use their site to get that data). Defaults to PROJECT_NAME.
        sheet_name (str, optional): Sheet name on Sheety (Use their site to get that data). Defaults to SHEET_NAME.

    Returns:
        dict: A dictionary with the recieved data.
    """
    
    request_headers = {
        "Authorization": SHEETY_AUTH_KEY,
    }
    
    response = requests.get(url = f"{SHEETY_ENDPOINT}/{SHEETY_USERNAME}/{project_name}/{sheet_name}", headers= request_headers)
    response.raise_for_status()
    
    data = response.json()
    
    return data

def add_row(row_data: dict, project_name: str = PROJECT_NAME, sheet_name: str = SHEET_NAME) -> None:
    """Function that add a row to the specified project sheet using the following API: "https://api.sheety.co".

    Args:
        row_data (dict): A dictionary with row data with key value pairs, where key = column name, value = value you want to insert in that column's new row.
        project_name (str, optional): Project name on Sheety (Use their site to get that data). Defaults to PROJECT_NAME.
        sheet_name (str, optional): Sheet name on Sheety (Use their site to get that data). Defaults to SHEET_NAME.
    """
    
    request_headers = {
        "Authorization": SHEETY_AUTH_KEY,
    }
    
    data = {
        sheet_name[:-1]: row_data,
    }
    
    response = requests.post(url = f"{SHEETY_ENDPOINT}/{SHEETY_USERNAME}/{project_name}/{sheet_name}", headers= request_headers, json = data)
    response.raise_for_status()
    
    # print(response.status_code)

# ------------------ MAIN ------------------ #
# Interpret the exercises entered by user and determine each exercise calories and duration
exercises_text = input("Tell me the Exercises you did:\n")
exercises = exercise_calories(exercises_text)

# Get current date and time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%d/%m/%Y")

# Add date and time to each exercise dictionary
for exercise in exercises:
    exercise["date"] = current_date
    exercise["time"] = current_time
    
    # Then add them a new row for each exercise in the spreadhseet
    add_row(exercise)