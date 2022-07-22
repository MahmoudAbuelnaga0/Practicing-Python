# Modules
import turtle
from food import Food

# Constants
PACE = 20
UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180
MAX = 280
MIN = -280

# Snake Class
class Snake:
    def __init__(self) -> None:
        self.create_snake()
        turtle.update()
        
    def create_snake(self):
        self.positions = [(0, 0), (-20, 0), (-40, 0)]
        self.body = []
        for position in self.positions:
            self.add_segment(position)
            
        self.head : turtle.Turtle = self.body[0]
        
    def add_segment(self, position):
        segment = turtle.Turtle("square")
        segment.penup()
        segment.color("white")
        segment.goto(position)
        self.body.append(segment)
        
    def forward(self):
        # Make the lower parts of snake follow the head
        for index in range(len(self.body)-1, 0, -1):
            new_pos = self.body[index - 1].pos()
            self.body[index].goto(new_pos)
        
        self.head.forward(PACE) # Move the head
        turtle.update()
        
    def up(self):
        if (self.head.heading() != DOWN):
            self.head.setheading(UP)
        
    def down(self):
        if (self.head.heading() != UP):
            self.head.setheading(DOWN)
        
    def left(self):
        if (self.head.heading() != RIGHT):
            self.head.setheading(LEFT)
        
    def right(self):
        if (self.head.heading() != LEFT):
            self.head.setheading(RIGHT)
            
    def touch_food(self, food: Food):
        distance = self.head.distance(food)
        return distance <= 20
        
    def hit_wall(self):
        condition = (self.head.xcor() > MAX) or (self.head.xcor() < MIN) or (self.head.ycor() > MAX) or (self.head.ycor() < MIN)
        return condition
    
    def extend(self):
        last_segment_pos = self.body[-1].pos()
        self.add_segment(last_segment_pos)
        
    def hit_tail(self):
        for index in range(1, len(self.body)):
            segment = self.body[index]
            distance = self.head.distance(segment)
            if (distance < 15):
                return True
            
        return False
    