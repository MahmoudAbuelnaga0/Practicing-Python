# Project Desciption:
#    This is a turtle race game where you ask the user to bet which turtle is going to win.
#    Steps:
#         1. Ask the user: ("Who will win the race? Enter a color: ") (on a pop up screen) <------
#             colors_list = ["pink", "blue", "green", "yellow", "orange", "red"]
            
#         2. Make the turtles race with different speeds (random speed for each turtle)
#             How to make that?
#             1. Generate different speed for each turtle by random module between (1 and 10) (until they reach the end line) 
#             2. All turtles generate at the center and go to their starting position at left <--------
#             3. Turtles move on screen with their specified speed (until someone reach the end line)   
#             4. print(which turtle won)

from turtle import Screen, Turtle
import random

def gen_race_turtles(colors: list = ["purple", "blue", "green", "yellow", "orange", "red"]) -> list:
    """Generate a list of turtle objects by the passed colors.

    Args:
        colors (list, optional): List of colors (Colors must be available in turtle module). Defaults to ["pink", "blue", "green", "yellow", "orange", "red"].

    Returns:
        list: Generated turtle objects
    """
    # Forming the turtle objects
    turtles = []
    for color in colors:
        turtle = Turtle()
        turtle.color(color)
        turtle.shape("turtle")
        turtle.penup()
        turtles.append(turtle)
        
    return turtles

def align_turtles(turtles: list) -> None:
    start_x = -230
    start_y = -120
    
    for turtle in turtles:
        turtle.goto(start_x, start_y)
        start_y += 50
        
def won(turtle: Turtle):
    return turtle.xcor() >= 230

# def random_forwarding(turtles: list):
#     for turtle in turtles:
#         forward_pace = random.randint(20, 70)
#         turtle.forward(forward_pace)
#     pass

def race(turtles: list) -> str:
    align_turtles(turtles)
    while(1):
        for turtle in turtles:
            forward_pace = random.randint(2, 8)
            turtle.forward(forward_pace)
            if (won(turtle)):
                pen = Turtle()
                pen.hideturtle()
                if(bet == turtle.color()[0]):
                    pen.write("You won!", font = ('Arial', 30, 'normal'), align="center")
                else:
                    pen.write("You lost!", font = ('Arial', 30, 'normal'), align="center")
                    
                return turtle.color()[0]




# Setting up screen
screen = Screen()
screen.setup(width = 500, height = 400)
screen.title("Turtle Betting Game")

# Displaying the prompt of the bet
colors: list = ["purple", "blue", "green", "yellow", "orange", "red"]
bet = screen.textinput("Bet", "Choose a color to place your bet (purple, yellow, green, blue, orange, red):")
if (bet is None):
    screen.bye()
    exit()

while (bet not in colors):
    bet = screen.textinput("Bet", "You must place a bet (purple, yellow, green, blue, orange, red):")
    if (bet is None):
        screen.bye()
        exit()

if (bet in colors):
    # Preparing the race turtles
    turtles = gen_race_turtles()

    # Start the race
    who_won = race(turtles)

    # Check if user's bet was right
    if(bet == who_won):
        msg = "You won!"
    else:
        msg = "You lost."
        
    msg = f"{msg} The {who_won} turtle is the winner."
    print(msg)
else:
    print("No bet was done.")
    
screen.exitonclick()