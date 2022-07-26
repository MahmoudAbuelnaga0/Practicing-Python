# Modules
from turtle import Screen, Turtle
from ball import Ball
from paddle import Paddle
from scoreboard import Scoreboard

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
LEFT_PADDLE_POS = (-450, 0)
RIGHT_PADDLE_POS = (450, 0)
MAX_SPEED_X = 6
MAX_SPEED_Y = 4

# Functions
def draw_line():
    # White line in the middle of screen
    pen = Turtle()
    pen.color("white")
    pen.hideturtle()
    pen.setheading(90)
    pen.pensize(10)
    pen.penup()
    pen.goto(0, -380)
    while (pen.ycor() <= 380):
        pen.pendown()
        pen.forward(50)
        pen.penup()
        pen.forward(50)

# Screen properties
screen = Screen()
screen.setup(width = SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.bgcolor("black")
screen.tracer(False)
draw_line()

# Screen objects
left_paddle = Paddle(LEFT_PADDLE_POS)
right_paddle = Paddle(RIGHT_PADDLE_POS)
ball = Ball()
scoreboard = Scoreboard()
screen.update()

# Game Functionality
screen.listen()
screen.onkey(fun = left_paddle.up, key = "w")
screen.onkey(fun = left_paddle.down, key = "s")
screen.onkey(fun = right_paddle.up, key = "Up")
screen.onkey(fun = right_paddle.down, key = "Down")

def play_game():
    ball.move()
    # Check if the ball hit walls
    if (ball.hit_upper_wall() or ball.hit_lower_wall()):
        ball.bounce_off_wall()
    
    # Check if the ball hit paddles
    if (ball.hit_left_paddle(left_paddle)):
        if (ball.first_time_hit_paddle):
            if (ball.speed_x < 0):
                update_speed_x = -MAX_SPEED_X
            else:
                update_speed_x = MAX_SPEED_X
                
            if (ball.speed_y < 0):
                update_speed_y = -MAX_SPEED_Y
            else:
                update_speed_y = MAX_SPEED_Y
            
            ball.update_speed(update_speed_x, update_speed_y)
            ball.first_time_hit_paddle = False
            
        ball.rebound_off_paddle(left_paddle)         
    elif (ball.hit_right_paddle(right_paddle)):
        if (ball.first_time_hit_paddle):
            if (ball.speed_x < 0):
                update_speed_x = -MAX_SPEED_X
            else:
                update_speed_x = MAX_SPEED_X
                
            if (ball.speed_y < 0):
                update_speed_y = -MAX_SPEED_Y
            else:
                update_speed_y = MAX_SPEED_Y
            
            ball.update_speed(update_speed_x, update_speed_y)
            ball.first_time_hit_paddle = False
            
        ball.rebound_off_paddle(right_paddle)
        
            
        
    if (ball.pass_left_boundary()):
        ball.reset_pos()
        scoreboard.update_scores("right")
    elif(ball.pass_right_boundary()):
        ball.reset_pos()
        scoreboard.update_scores("left")
             
    screen.update()
    screen.ontimer(play_game, 2)

play_game()


screen.exitonclick()