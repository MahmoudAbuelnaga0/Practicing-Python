import turtle
import datetime
class Scoreboard(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__()
        self.score = 0
        
        # Getting latest high score from HighScores file
        with open("HighScores.txt", mode = "r") as file:
            contents = file.read()
            contents = contents.split("\n")
            latest_record = contents[-1]
            self.high_score = int(latest_record[latest_record.index(">")+2: ])
            
        self.hideturtle()
        self.pencolor("white")
        self.penup()
        self.goto(0, 270)
        self.show_score()
        
    def show_score(self):
        self.clear()
        self.write(arg = f"Score: {self.score}      High Score: {self.high_score}", align = "center", font = ("Arial", 15, 'normal'))
        
    def inc_score(self):
        self.score += 1
        self.show_score()
        
    def reset(self):
        self.score = 0
        self.show_score()
        
    def got_new_high_score(self):
        return self.score > self.high_score
    
    def update_high_score(self):
        self.high_score = self.score
        
    def save_high_score(self):
        with open("HighScores.txt", mode = "a") as file:
            current_time = datetime.datetime.now()
            day = current_time.day
            month = current_time.month
            year = current_time.year
            hour = current_time.hour
            minute = current_time.minute
            file.write(f"\n{day}/{month}/{year} {hour}:{minute} --> {self.high_score}")