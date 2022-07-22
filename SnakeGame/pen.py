import turtle

class Pen(turtle.Turtle):
    def __init__(self, color) -> None:
        super().__init__()
        self.hideturtle()
        self.pencolor(color)
        self.penup()