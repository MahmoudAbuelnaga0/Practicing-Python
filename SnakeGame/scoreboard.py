import turtle

class Scoreboard(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.score = -1
        self.hideturtle()
        self.pencolor("white")
        self.penup()
        self.goto(0, 270)
        self.update()
        
    def update(self):
        self.score += 1
        self.clear()
        self.write(arg = f"Score: {self.score}", align = "center", font = ("Arial", 15, 'normal'))