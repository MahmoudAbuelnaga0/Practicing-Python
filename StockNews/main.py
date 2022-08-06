# ------------- MODULES ------------- #
import requests
import os
from itertools import islice
from twilio.rest import Client
from html import unescape

# ------------- CONSTANTS------------- #
COMPANY_SYMBOL = "TSLA"
COMPANY_NAME = "Tesla"

AV_ENDPOINT = "https://www.alphavantage.co/query"
AV_API_KEY = ""

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = ""

TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
TWILIO_VERIFIED_NUMBER = ""

UP_CHART = "📈"
DOWN_ARROW = "🔻"

# ------------- FUNCTIONS ------------- #
def get_daily_stocks(company_symbol: str = COMPANY_SYMBOL) -> dict:
    """Function that connects to AlphaVantage API and get the daily stocks data of required company.

    Args:
        company_symbol (str, optional): Company Symbol. Defaults to COMPANY_SYMBOL.

    Returns:
        dict: dictionary of stocks data where key: Date string & value: Stocks details dictionary with (1. open, 2. high, 3. low, 4. close, 5. volume) as keys
    """
    try:
        api_key = os.environ["AV_API_KEY"]
    except KeyError:
        api_key = AV_API_KEY
        
    parameters = {
        "function": "TIME_SERIES_DAILY",    # The data that I nedd
        "symbol": company_symbol,    # Company name
        "apikey": api_key,
    }
    
    response = requests.get(url = AV_ENDPOINT, params= parameters)
    response.raise_for_status()
    
    response_data = response.json()
    daily_data = response_data["Time Series (Daily)"]
    return daily_data

def slice(iterable: dict, n: int = 2) -> list:
    """Function that gets the latest n-values of dictionary.

    Args:
        iterable (dict): the dictionary that we want slice.
        n (int, optional): Length of returned list. Defaults to 2.

    Returns:
        list: List of first n-values of dictionary (Values not Keys).
    """
    return list(islice(iterable.values(), n))
    
def calc_change_perc(data: list, value_name: str = "4. close") -> float:
    """Calculates the change percentage for the specified value_name from the data passed.

    Args:
        data (list): List of dictionaries that contains recent stocks data.
        value_name (str, optional): The value you want to calculate the change percentage for. Defaults to "4. close".

    Returns:
        float: The change percentage.
    """
    first_value = float(data[0][value_name])
    second_value = float(data[1][value_name])
    perc= ((first_value - second_value)/first_value) * 100
    return perc

def get_news(company_name: str = COMPANY_NAME) -> str:
    """Connects to News API and get the latest 3 news about the company entered as an argument.

    Args:
        company_name (str, optional): Company you want to get news about. Defaults to COMPANY_NAME.

    Returns:
        str: A string with the latest 3 news title and brief description. 
    """
    # API KEY
    try:
        api_key = os.environ["NEWS_API_KEY"]
    except KeyError:
        api_key = NEWS_API_KEY
        
    # PARAMETERS
    parameters = {
        "q": company_name,
        "apikey": api_key,
        "sortBy": "popularity",
        "pageSize": 3,  # No of returned articles
        "searchIn": "title",
    }
    # SEND REQUEST TO THE ENDPOINT
    response = requests.get(url = NEWS_ENDPOINT, params= parameters)
    response.raise_for_status() # check if there was error in request
    
    # GET REQUEST ARTICLES
    articles = response.json()["articles"]
    
    # NEWS STRING 
    news = "News:\n"
    n = 1
    for article in articles:
        title = unescape(article["title"])
        description = unescape(article["description"])
        news += f"{n}. Headline: {title}\nBrief: {description}\n\n"
        n += 1
        
    return news

def send_message(message: str) -> str:
    """Connect to Twilio API and send a message.

    Args:
        message (str): The message to send.

    Returns:
        str: Status of the operation.
    """
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        account_number = os.environ["ACCOUNT_NUMBER"]
        my_number = os.environ["MY_NUMBER"]
    except KeyError:
        account_sid = TWILIO_SID
        auth_token = TWILIO_AUTH_TOKEN
        account_number = TWILIO_PHONE_NUMBER
        my_number = TWILIO_VERIFIED_NUMBER
        
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(
        body = message,
        from_ = account_number,
        to = my_number,
    )
    
    return message.status
    
# ------------- MAIN ------------- #
company_daily_stocks = get_daily_stocks()   # Get daily stocks data for the desired company (Tesla)
latest_data = slice(company_daily_stocks)   # Get the data of the latest 2 dates stocks

change_perc = calc_change_perc(latest_data) # Calculate percentage of change in close values (change default value if you want to calculate change of another data value.)
# If the change percentage is greater than or equal 5 notify me
if(abs(change_perc) >= 5):
    # Prepare message to send
    if (change_perc > 0):
        msg = f"{COMPANY_NAME.upper()}:{UP_CHART}{round(change_perc)}%\n"
    else:
        msg  = f"{COMPANY_NAME.upper()}:{DOWN_ARROW}{round(abs(change_perc))}%\n"
        
    news = get_news()
    msg += news
    
    status = send_message(msg)
    print(status)