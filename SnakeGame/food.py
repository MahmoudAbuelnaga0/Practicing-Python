import turtle
import random

class Food(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__("circle")
        self.penup()
        self.shapesize(stretch_len= 0.5, stretch_wid=0.5)
        self.color("blue")
        self.random_pos()
        turtle.update()
        
    def random_pos(self):
        random_x = random.randint(-270, 270)
        random_y = random.randint(-270, 260)
        self.goto(random_x, random_y)
    