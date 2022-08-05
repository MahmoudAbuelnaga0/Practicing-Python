import requests

def get_questions(num_questions: int = 10) -> list:
    """Function that connect to Trivia API and get a number of computer science True or False questions

    Args:
        num_questions (int, optional): Num of question you want to get. Defaults to 10.

    Returns:
        list: List of questions got from Trivia API
    """
    request_parameters = {
        "amount": num_questions,
        "category": 18,
        "type": "boolean",
    }
    
    response = requests.get(url = "https://opentdb.com/api.php", params= request_parameters)
    response.raise_for_status()
    
    questions = response.json()["results"]
    return questions

question_data = get_questions()