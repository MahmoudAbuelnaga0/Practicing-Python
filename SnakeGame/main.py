# Modules
import time
from turtle import Screen
from scoreboard import Scoreboard
from snake import Snake
from food import Food
from pen import Pen

# GAME FUNCTIONS
def restart_game():
    global food
    screen.clear()
    screen.tracer(0)    # Update screen manually
    screen.bgcolor("black")
       
    # Screen listens to keyboard presses
    screen.listen()
    screen.onkey(fun = snake.up, key="Up")  # Press Up to move up
    screen.onkey(fun = snake.down, key="Down")  # Press down to move down
    screen.onkey(fun = snake.left, key="Left")  # Press left to move left
    screen.onkey(fun = snake.right, key="Right")    # Press right to move right
    
    scoreboard.reset()
    snake.reset()
    food = Food()

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
        scoreboard.inc_score() # Scoreboard increases
        screen.update() # Update the screen
        
    # Detect collision with a wall or tail
    if (snake.hit_wall() or snake.hit_tail()):
        if (scoreboard.got_new_high_score()):
            scoreboard.update_high_score()
            scoreboard.save_high_score()
        
        # Checking if user want to play again
        ans = screen.textinput("GAME OVER!", "Would you like to play again? ('Y'/'N')")
        if (ans is not None):
            ans = ans.upper()
            
        if (ans == "Y"):
            restart_game()
        else:
            game_is_on = False
            pen.write("GAME OVER!", align = "center", font = ("Arial", 15, 'normal'))
                         
    # Wait 0.1 sec before the snake moves a step forward
    time.sleep(0.1)

screen.exitonclick()