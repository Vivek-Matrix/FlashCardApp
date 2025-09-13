from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_pic)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word,text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_pic)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=536)
card_front_pic = PhotoImage(file="images/card_front.png")
card_back_pic = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_pic)


title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400,263, text="word", font=("Ariel",40,"bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0,column=0, columnspan=2)

wrong=PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong, command=is_known)
wrong_button.grid(row=1,column=0)

right=PhotoImage(file="images/right.png")
right_button = Button(image=right, command=next_card)
right_button.grid(row=1,column=1)



next_card()

window.mainloop()