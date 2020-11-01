# Environment setup commands:
# olympe: source ~/code/parrot-groundsdk/./products/olympe/linux/env/shell
import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import olympe
import subprocess
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, PCMD
from collections import defaultdict
# from enum import Enum

# Drone flight state variables
is_connected = False

# Drone constants
DRONE_IP = "192.168.42.1"
SPHINX_IP = "10.202.0.1"

# UI Global variables
HEIGHT = 600
WIDTH = 800
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
ROTATE_BUTTON_WIDTH = 70
ROTATE_BUTTON_HEIGHT = 400

# Control variables
control_quit = 0
control_takeoff = 1

# Button helper functions
# Roll drone to the left 
def roll_left():
    drone(
        PCMD(
            1,
            -10,
            0,
            0,
            0,
            10,
        )
    ) 

# Roll drone to the right 
def roll_right():
    drone(
        PCMD(
            1,
            10,
            0,
            0,
            0,
            10,
        )
    )

# Pitch the drone forward (move forward)
def pitch_fwd():
    drone(
        PCMD(
            1,
            0,
            10,
            0,
            0,
            10,
        )
    )

# Pitch drone backward (move backward)
def pitch_back():
    drone(
        PCMD(
            1,
            0,
            -10,
            0,
            0,
            10,
        )
    )

# Spin drone to the left 
def turn_left():
    drone(
        PCMD(
            1,
            0,
            0,
            -10,
            0,
            10,
        )
    )

# Turn drone to the right
def turn_right():
    drone(
        PCMD(
            1,
            0,
            0,
            10,
            0,
            10,
        )
    )

# Takeoff routine
def takeoff():
    # Connect to the drone's Wi-Fi access point if necessary
    global is_connected
    if not is_connected:
        drone.connect()
        is_connected = True
    assert drone(TakeOff()).wait().success()
        

# Landing routine
def land():
    # Escape if not connected to the drone
    global is_connected
    if is_connected:
        assert drone(Landing()).wait().success()
    



# setting up screen
root = tk.Tk()
root.resizable(False, False)
root.title("Anafi Drone GUI")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

title = tk.Label(canvas, text="Flight Controller v1",
                 font=('Century', 20), anchor='center')
title.place(relx=0.15, rely=0.02, relwidth=0.7, relheight=0.1)

controlFrame = tk.Frame(root)
controlFrame.place(relwidth=0.9, relheight=0.7, relx=0.05, rely=0.15)

# # setting up the slider
# var = DoubleVar()
# scale = Scale(controlFrame, variable=var, from_=50, to=-50)
# scale.place(relwidth=0.2, relheight=0.9, relx=0.3, rely=0.05)

# # left button
# left_button_image = Image.open("Left_button.png")
# left_img = left_button_image.resize(
#     (BUTTON_WIDTH, BUTTON_HEIGHT), Image.ANTIALIAS)
# left_photoImg = ImageTk.PhotoImage(left_img)
# leftbutton = Button(controlFrame, image=left_photoImg, command=roll_left)
# leftbutton.place(relwidth=0.075, relheight=0.1, relx=0.5, rely=0.4)

# # right button
# right_button_image = Image.open("Right_Button.png")
# right_img = right_button_image.resize(
#     (BUTTON_WIDTH, BUTTON_HEIGHT), Image.ANTIALIAS)
# right_photoImg = ImageTk.PhotoImage(right_img)
# rightbutton = Button(controlFrame, image=right_photoImg, command=roll_right)
# rightbutton.place(relwidth=0.075, relheight=0.1, relx=0.7, rely=0.4)

# # top button
# top_button_image = Image.open("Up_Button.png")
# top_img = top_button_image.resize(
#     (BUTTON_WIDTH, BUTTON_HEIGHT), Image.ANTIALIAS)
# top_photoImg = ImageTk.PhotoImage(top_img)
# topbutton = Button(controlFrame, image=top_photoImg, command=pitch_fwd)
# topbutton.place(relwidth=0.075, relheight=0.1, relx=0.6, rely=0.2)

# # down button
# down_button_image = Image.open("Down_button.png")
# down_img = down_button_image.resize(
#     (BUTTON_WIDTH, BUTTON_HEIGHT), Image.ANTIALIAS)
# down_photoImg = ImageTk.PhotoImage(down_img)
# downbutton = Button(controlFrame, image=down_photoImg, command=pitch_back)
# downbutton.place(relwidth=0.075, relheight=0.1, relx=0.6, rely=0.6)

# rotate left
l_rotate_button_image = Image.open("Left_Rotate.png")
l_rotate_img = l_rotate_button_image.resize(
    (ROTATE_BUTTON_WIDTH, ROTATE_BUTTON_HEIGHT), Image.ANTIALIAS)
l_rotate_photoImg = ImageTk.PhotoImage(l_rotate_img)
l_rotate_button = Button(controlFrame, image=l_rotate_photoImg, command=turn_left)
l_rotate_button.place(relwidth=0.1, relheight=0.8, relx=0.1, rely=0.1)

# rotate right
r_rotate_button_image = Image.open("Right_Rotate.png")
r_rotate_img = r_rotate_button_image.resize(
    (ROTATE_BUTTON_WIDTH, ROTATE_BUTTON_HEIGHT), Image.ANTIALIAS)
r_rotate_photoImg = ImageTk.PhotoImage(r_rotate_img)
r_rotate_button = Button(
    controlFrame, image=r_rotate_photoImg, command=turn_right)
r_rotate_button.place(relwidth=0.1, relheight=0.8, relx=0.8, rely=0.1)

# takeoff button
takeoff_button = tk.Button(controlFrame, text ="Takeoff", command=takeoff)
takeoff_button.place(relwidth=0.075, relheight=0.1, relx=0.5, rely=0.4)

# landing button
landing_button = tk.Button(controlFrame, text ="Land", command=land)
landing_button.place(relwidth=0.075, relheight=0.1, relx=0.7, rely=0.4)


# Main Loop Start:

if __name__ == "__main__":
    with olympe.Drone(SPHINX_IP) as drone:
        root.mainloop()