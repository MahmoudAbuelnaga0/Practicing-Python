# Modules
import turtle
from paddle import Paddle

# Constants
UPPER_LIMIT = 385
LOWER_LIMIT = -385
LEFT_BOUNDARY = -490
RIGHT_BOUNDARY = 490
START_SPEED_X = 3
START_SPEED_Y = 1

# Class definition
class Ball(turtle.Turtle):
    def __init__(self) -> None:
        super().__init__("circle")
        self.color("white")
        self.penup()
        self.speed_x = START_SPEED_X
        self.speed_y = START_SPEED_Y
        self.first_time_hit_paddle = True
        
    def move(self):
        new_x = self.xcor() + self.speed_x
        new_y = self.ycor() + self.speed_y
        self.goto(new_x, new_y)
        
    def hit_upper_wall(self):
        condition = (self.ycor() > UPPER_LIMIT)
        return condition
    
    def hit_lower_wall(self):
        condition = (self.ycor() < LOWER_LIMIT)
        return condition
    
    def bounce_off_wall(self):
        self.speed_y = -self.speed_y
   
    def rebound_off_paddle(self, paddle: Paddle = None):
        # # Use case you wanted to make the ball go up or down based on the place that ball hit the paddle
        # if (self.ycor() > paddle.ycor()):
        #     self.speed_y = abs(self.speed_y)
        # elif(self.ycor() <= paddle.ycor()):
        #     if (self.speed_y > 0):
        #         self.speed_y = -self.speed_y
                            
        self.speed_x = -self.speed_x
        
    def hit_paddle(self, paddle: Paddle):
        distance_x = abs(self.xcor() - paddle.xcor())
        distance_y = abs(self.ycor() - paddle.ycor())
        
        # Prevent rebound off back of paddle
        if (paddle.xcor() > 0): # Right paddle
            paddle_condition = self.xcor() < paddle.xcor()
        else:   # Left paddle
            paddle_condition = self.xcor() > paddle.xcor()
            
        return (distance_x <= 20) and (distance_y <= 50) and paddle_condition
        
    def pass_left_boundary(self):
        return self.xcor() < LEFT_BOUNDARY
    
    def pass_right_boundary(self):
        return self.xcor() > RIGHT_BOUNDARY
    
    def update_speed(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
        
    def reset_pos(self):
        self.home()
        if (self.speed_x > 0):
            self.update_speed(-START_SPEED_X, START_SPEED_Y)
        else:
            self.update_speed(START_SPEED_X, START_SPEED_Y)       
        self.first_time_hit_paddle = True