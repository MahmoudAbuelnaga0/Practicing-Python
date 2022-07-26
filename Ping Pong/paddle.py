# Modules
from turtle import Turtle

# Constants
PACE = 40
UPPER_LIMIT = 340
LOWER_LIMIT = -340


# Class definition
class Paddle(Turtle):
    def __init__(self, start_position: tuple) -> None:
        super().__init__("square")
        self.color("white")
        self.penup()
        self.setpos(start_position)
        self.setheading(90)
        self.shapesize(stretch_len=4.5)
        self.width_xcors()
        self.edges_ycors()
        
    def down(self):
        if (not(self.down_lower_limit())):
            self.backward(PACE)
            self.edges_ycors()
              
    def up(self):
        if (not(self.over_upper_limit())):
            self.forward(PACE)
            self.edges_ycors()
        
    def over_upper_limit(self):
        condition = (self.ycor() > UPPER_LIMIT)
        return condition
    
    def down_lower_limit(self):
        condition = (self.ycor() < LOWER_LIMIT)
        return condition
    
    def width_xcors(self):
        if (self.xcor() > 0):
            self.F_face_xcor = self.xcor() - 10
            self.B_face_xcor = self.xcor() + 10
        else:
            self.F_face_xcor = self.xcor() + 10
            self.B_face_xcor = self.xcor() - 10
            
    def edges_ycors(self):
        self.U_edge_ycor = self.ycor() + 45
        self.L_edge_ycor = self.ycor() - 45
    
    
    
    
    
        
        
    
