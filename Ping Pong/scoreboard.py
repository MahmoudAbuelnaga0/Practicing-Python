from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self) -> None:
        # Turtle properties
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, 350)
        
        self.left_score = 0
        self.right_score = 0
        self.update_scores()
        
    def update_scores(self, side: str = None):
        if (side == "left"):
            self.left_score += 1
        elif (side == "right"):
            self.right_score += 1
            
        self.clear()
        self.write(arg = f"{self.left_score}        {self.right_score}", align = "center", font = ('Courier', 35, 'bold'))
        