# Modules
from dis import dis
from turtle import Turtle, distance
from car import Car

# Constants
UPPER_LIMIT = 340
LOWER_LIMIT = -330
LEFT_LIMIT = -330
RIGHT_LIMIT = 330
PACE = 10

# Class definition
class Player(Turtle):
    def __init__(self) -> None:
        # Defining player appearance
        super().__init__("turtle")
        self.color("black")
        self.penup()
        self.goto(0, LOWER_LIMIT)
        self.setheading(90)
        
    def go_up(self):
        self.forward(PACE)
        
    def go_down(self):
        if (self.ycor() > LOWER_LIMIT):
            self.backward(PACE)
        
    def go_left(self):
        if(self.xcor() > LEFT_LIMIT):
            self.setx(self.xcor() - PACE)
        
    def go_right(self):
        if(self.xcor() < RIGHT_LIMIT):
            self.setx(self.xcor() + PACE)
            
    def reach_end(self):
        return self.ycor() > UPPER_LIMIT
    
    def hit_car(self, car: Car): 
        distance_x = abs(self.xcor() - car.xcor())
        distance_y = abs(self.ycor() - car.ycor())
        return (distance_x < 40) and (distance_y < 23)
        
    
     