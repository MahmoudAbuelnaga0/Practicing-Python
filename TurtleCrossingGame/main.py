# Modules
from turtle import Screen
from car import Car
from player import Player
from scoreboard import Scoreboard

#Screen Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Screen properties
screen = Screen()
screen.setup(width = SCREEN_WIDTH, height= SCREEN_HEIGHT)
screen.tracer(False)

# GAME FUNCTION
scoreboard = Scoreboard()
no_of_cars = 15
time = 300
car_speed = 0.2
def play_game():
    # Global variables
    global no_of_cars
    global time
    global car_speed
    global scoreboard
    
    screen.tracer(False)
    # Screen Objects
    player = Player()
    cars = []   # A list to contain cars generated on screen
    scoreboard.show_level()
    screen.update()
    
    # Game Functions
    def move_cars():
        for car in cars:
            car.move()
            if (car.reach_end()):
                car.reset_car()
        
    def create_cars():
        if (len(cars) <= no_of_cars):
            vechile = Car(car_speed)
            cars.append(vechile)
            screen.ontimer(fun = create_cars, t = time)
    
    # Player Movement
    screen.listen()
    screen.onkeypress(fun = player.go_up, key = "Up")
    screen.onkeypress(fun = player.go_down, key = "Down")
    screen.onkeypress(fun = player.go_left, key = "Left")
    screen.onkeypress(fun = player.go_right, key = "Right")
    
    # Game Loop
    game_is_on = True
    create_cars()
    while (game_is_on):
        move_cars() # Move cars of game
        screen.update()
        # Check if player hit a car
        for car in cars:
            if (player.hit_car(car)):
                game_is_on = False
                scoreboard.end_game()
                break
        
        # Check if player reached the end line
        if (player.reach_end()):
            # Inc difficulty
            no_of_cars += 2
            time -= 20
            car_speed += 0.1
            scoreboard.inc_level()
            # Clear screen
            screen.clear()
            # Delete old variables
            del cars
            del player
            # Start game with the new difficulty
            play_game()
            game_is_on = False

# STARTING THE GAME
play_game()

screen.exitonclick()