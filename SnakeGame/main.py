# Modules
import time
from turtle import Screen
from scoreboard import Scoreboard
from snake import Snake
from food import Food
from pen import Pen

# Screen Properties
screen = Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)    # Update screen manually

# Game objects
snake = Snake()
food = Food()
scoreboard = Scoreboard()
pen = Pen("red")
game_is_on = True

# Screen listens to keyboard presses
screen.listen()
screen.onkey(fun = snake.up, key="Up")  # Press Up to move up
screen.onkey(fun = snake.down, key="Down")  # Press down to move down
screen.onkey(fun = snake.left, key="Left")  # Press left to move left
screen.onkey(fun = snake.right, key="Right")    # Press right to move right

# Game loop
while(game_is_on):      
    snake.forward()
    
    # Snake touches food
    if(snake.touch_food(food)):
        food.random_pos()   # Food goes to random position
        snake.extend()
        scoreboard.update() # Scoreboard increases
        screen.update() # Update the screen
        
    # Detect collision with a wall or tail
    if (snake.hit_wall() or snake.hit_tail()):
        pen.write("GAME OVER!", align = "center", font = ("Arial", 15, 'normal'))
        game_is_on = False
              
    # Wait 0.1 sec before the snake moves a step forward
    time.sleep(0.1)


screen.exitonclick()