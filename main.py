from tkinter import *
from tkinter import PhotoImage
import os

import pandas
import random
import pyttsx3


BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashyy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50, highlightthickness=0)


# --------------------------- DISPLAY VOCABULARY ----------------------------- #
engine = pyttsx3.init()
current_card = {}


def check_data_file():
    if not os.path.exists("./data/words_to_learn.csv"):
        try:
            prev_data = pandas.read_csv("./data/Flash Card Project.csv")
            prev_data.to_csv("./data/words_to_learn.csv", index=False)
        except FileNotFoundError:
            print("Source CSV file is missing.")

def next_card():
    global flip_timer, current_card
    window.after_cancel(flip_timer)
    try:
        check_data_file()
        canvas.itemconfig(img, image=frontside_img_file)
        new_data = pandas.read_csv("./data/words_to_learn.csv")
        data_dict = new_data.to_dict(orient="records")
        current_card = random.choice(data_dict)
    except IndexError:
        canvas.itemconfig(card_word, text="There are no words left :)", fill="black")
    else:
        canvas.itemconfig(card_title, text="Kor", fill="black")
        canvas.itemconfig(card_word, text=current_card["Korean"], fill="black")
        flip_timer = window.after(3000, flip_card,current_card)
        return current_card

def flip_card(word):
    canvas.delete()
    canvas.itemconfig(img, image=backside_img_file)
    canvas.itemconfig(card_title, text="Eng", fill="white")
    canvas.itemconfig(card_word, text=word["English"], fill="white")

flip_timer = window.after(3000, flip_card)

def pronounce_word():
    engine.say(current_card["English"])
    engine.runAndWait()

def check_btn_clicked():
    current_word = next_card()
    words_df = pandas.read_csv("./data/words_to_learn.csv")
    updated_df = words_df[words_df["Korean"] != current_word["Korean"]]
    updated_df.to_csv("./data/words_to_learn.csv", index=False)


# ---------------------------- USER INTERFACE --------------------------------- #

# IMAGES
canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0, highlightbackground=BACKGROUND_COLOR)
frontside_img_file: PhotoImage = PhotoImage(file="./images/card_front.png")
backside_img_file = PhotoImage(file="./images/card_back.png")

img = canvas.create_image(400, 263, image=frontside_img_file)

card_title = canvas.create_text(400, 150, text="", font=("Arial", 30, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Arial", 55, "bold"), fill="black")
canvas.grid(row=0, column=0, columnspan=2)

# back_side_img = PhotoImage(file="card_back.png")
# canvas.create_image(400, 526 / 2, image="front_side_img")

x_sign_img = PhotoImage(file="./images/wrong.png")
check_sign_img = PhotoImage(file="./images/right.png")
speaker_img = PhotoImage(file="./images/speaker.png")


# BUTTONS
x_btn = Button(image=x_sign_img, padx=100, pady=90, highlightbackground=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
x_btn.grid(row=1, column=0)

y_btn = Button(image=check_sign_img, width=100, height=90, highlightbackground=BACKGROUND_COLOR, highlightthickness=0, command=check_btn_clicked)
y_btn.grid(row=1, column=1)

speaker_btn = Button(width=30, height=27, image=speaker_img, bg="black", highlightbackground="white", command=pronounce_word)
speaker_btn.place(x=382, y=350)

next_card()


window.mainloop()


