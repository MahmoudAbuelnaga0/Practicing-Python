from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("black")
        self.goto(-310, 310)
        self.level = 1
        self.show_level()
        
    def show_level(self):
        self.clear()
        self.write(f"Level: {self.level}", align="left", font = ("Courier", 20, 'normal'))
        
    def inc_level(self):
        self.level += 1
        
    def end_game(self):
        self.goto(0, 0)
        self.write("GAME OVER!", align = "center", font = ("Courier", 20, 'normal'))