# MODULES
from cgitb import text
from tkinter import *
from quiz_brain import QuizBrain
from time import sleep

# CONSTANTS
THEME_COLOR = "#375362"
WHITE = "#FFFFFF"
GREEN = "#00FF00"
RED = "#FF0000"
BLACK = "#000000"

class QuizUI:
    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.score = 0
        self.quiz_brain = quiz_brain
        # SETUP THE WINDOW
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx = 20, pady = 20, bg = THEME_COLOR)
        
        # SCORE LABEL
        self.score_label = Label(text = f"Score: {self.score}", fg= WHITE, bg = THEME_COLOR, font=("Arial", 15, "normal"), justify="right")
        self.score_label.grid(row = 0, column= 1)
        
        # CANVAS AND QUESTION TEXT
        self.canvas = Canvas(width= 500, height= 450, bg = WHITE)
        self.canvas.grid(row = 1, column= 0, columnspan= 2, pady= 50)
        self.question_text = self.canvas.create_text(250, 225, fill = THEME_COLOR, width=450, font= ("Arial", 20, "normal"))
        
        # RIGHT AND WRONG BUTTONS
        true_img = PhotoImage(file = "./images/true.png")
        self.true_button = Button(image = true_img, highlightthickness= 0, command= lambda answer = "True": self.check_ans(answer))
        self.true_button.grid(row = 2, column= 0)
        
        false_img = PhotoImage(file="./images/false.png")
        self.false_button = Button(image = false_img, highlightthickness= 0, command= lambda answer = "False": self.check_ans(answer))
        self.false_button.grid(row = 2, column= 1)
        
        self.show_next_question()
        self.window.mainloop()
        
    def show_next_question(self) -> None:
        self.canvas.config(bg = WHITE)
        self.canvas.itemconfig(self.question_text, fill = THEME_COLOR)
        question_text = self.quiz_brain.next_question()
        self.canvas.itemconfig(self.question_text, text = question_text)
        self.window.update()
        
    def check_ans(self, ans: bool) -> None:
        self.disable_buttons()
        if (self.quiz_brain.is_right(ans)):
            self.score += 1
            self.score_label.config(text= f"Score: {self.score}")
            self.canvas.config(bg= GREEN)
        else:
            self.canvas.config(bg= RED)
        
        self.canvas.itemconfig(self.question_text, fill = BLACK)
        self.window.update()
        sleep(1.3)
        if (self.quiz_brain.still_has_questions()):
            self.show_next_question()
            self.enable_buttons()
        else:
            self.canvas.config(bg = WHITE)
            self.canvas.itemconfig(self.question_text, fill = BLACK, text = f"Your final score is:\n{self.score} out of {len(self.quiz_brain.question_list)}", justify = "center")
        
    def no_fun(self):
        pass
            
    def disable_buttons(self):
        self.true_button.config(command= self.no_fun)
        self.false_button.config(command= self.no_fun)
        
    def enable_buttons(self):
        self.true_button.config(command= lambda answer = "True": self.check_ans(answer))
        self.false_button.config(command= lambda answer = "False": self.check_ans(answer))
        
            