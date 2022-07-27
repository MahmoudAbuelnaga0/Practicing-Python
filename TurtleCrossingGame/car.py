# Modules
from turtle import Turtle
import random

# Constants
CAR_COLORS = ["orange", "red", "green", "blue", "violet"]
UPPER_LIMIT = 300
LOWER_LIMIT = -290
LEFT_LIMIT = -390
RIGHT_LIMIT = 380

# Class definition
class Car(Turtle):
    def __init__(self, speed) -> None:
        # Defining appearance and properties
        super().__init__("square")
        self.color(random.choice(CAR_COLORS))
        self.setheading(180)
        self.shapesize(stretch_len= 3)
        self.penup()
        self.pace = speed
        self.reset_car()
        
    def move(self):
        self.forward(self.pace)
        # self.update_length_limits()
        
    def reach_end(self):
        return self.xcor() < LEFT_LIMIT
    
    def reset_car(self):
        # Picking random position to go to
        random_y = random.randint(LOWER_LIMIT, UPPER_LIMIT)
        self.setpos(RIGHT_LIMIT, random_y)