# Modules
from tkinter import ttk
from tkinter import *
import pandas as pd
import random

# Constants and important variables
BACKGROUND_COLOR = "#B1DDC6"
FRONT_FACE_LANG = "French"
BACK_FACE_LANG = "English"
word = None # Variable which holds the words we are currently showing
displayed_text = ""

# Functions
def show_front_face():
    front_face_word = word[FRONT_FACE_LANG]
    canvas.itemconfig(current_img, image = card_front_img)
    canvas.itemconfig(current_text, text = f"{FRONT_FACE_LANG}\n\n{front_face_word}")
    
def show_back_face():
    back_face_word = word[BACK_FACE_LANG]
    canvas.itemconfig(current_img, image = card_back_img)
    canvas.itemconfig(current_text, text = f"{BACK_FACE_LANG}\n\n{back_face_word}")

def flip(event) -> None:
    """Function that shows other side of flashcard"""
    
    current_img_name = canvas.itemcget(current_img, "image")    # Get the name of current image
    # Change the current image on canvas
    if (current_img_name == "pyimage1"):    # If we are at front face which shows first language
        show_back_face()
    elif (current_img_name == "pyimage2"):  # if we are at back face
        show_front_face()
        
def no_flip(event):
    pass
     
def next_word():
    """Shows the next word on GUI"""
    
    global word
    try:
        word = random.choice(words_data)
    except:
        canvas.itemconfig(current_text, text = f"No words left")
        canvas.bind("<Button-1>", no_flip)
    else:
        show_front_face()
        
def right():
    global words_data
    try:
        word_index = words_data.index(word)
    except ValueError:
        canvas.itemconfig(current_text, text = f"No words left")
        canvas.bind("<Button-1>", no_flip)
    else:
        del words_data[word_index]
        next_word()
        
def get_words_data() -> list:
    """Function to read data from csv"""
    
    # Reading data out of csv file
    try:
        words_data = pd.read_csv("./data/words_to_learn.csv")   
    except:
        words_data = pd.read_csv("./data/french_words.csv")
    finally:
        # Extract required data based on languages needed
        words_list = words_data.to_dict("records")
        return words_list

# -------------------------- FLASHCARDS DATA -------------------------- #
words_data = get_words_data()

# -------------------------- UI -------------------------- #
# Display window
window = Tk()
window.title("Flashcards")
window.config(bg = BACKGROUND_COLOR, padx = 50, pady = 50)

# Canvas Setup
canvas = Canvas(bg = BACKGROUND_COLOR, width = 800, height = 526, highlightthickness=0)
# Canvas images
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
# Applying back image and showing word text
current_img = canvas.create_image(400, 263, image = card_front_img)
current_text = canvas.create_text(400, 200, text="", font = ("Arial", 40, "normal"), justify="center")
next_word()
# Binding mouse click to the canvas
canvas.bind("<Button-1>", flip)
# Show canvas
canvas.grid(row = 0, column = 0, columnspan= 2)

# Wrong Button
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = ttk.Button(image = wrong_img, command=next_word)
wrong_button.grid(row = 1, column= 0)
# Right Button
right_img = PhotoImage(file="./images/right.png")
right_button = ttk.Button(image = right_img, command=right)
right_button.grid(row = 1, column= 1)

window.mainloop()

# After the user closes the window
word_to_learn = pd.DataFrame(words_data)
word_to_learn.to_csv("./data/words_to_learn.csv", index=False)