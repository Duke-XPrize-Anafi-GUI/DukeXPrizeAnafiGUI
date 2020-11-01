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
from olympe.messages.ardrone3.PilotingSettingsState import MaxTiltChanged
import olympe.messages.gimbal as gimbal
# from enum import Enum

# Drone flight state variables
is_connected = False

# Drone constants
DRONE_IP = "192.168.42.1"
SPHINX_IP = "10.202.0.1"

# UI Global variables
HEIGHT = 720
WIDTH = 1280
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

def increase_throttle():
    drone(
        PCMD(
            0,
            0,
            0,
            0,
            10,
            10,
        )
    )

def decrease_throttle():
    drone(
        PCMD(
            0,
            0,
            0,
            0,
            -10,
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

def move_forward():
    print("Drone MaxTilt = ", drone.get_state(MaxTiltChanged))
    drone(
        gimbal.set_target(
            gimbal_id = 0,
            control_mode = "position",
            yaw_frame_of_reference = "absolute",
            yaw = 0.0,
            pitch_frame_of_reference = "relative",
            pitch = -10,
            roll_frame_of_reference = "absolute",
            roll = 0.0
        )
    ).wait()
    # drone(
    #     PCMD(
    #         0,
    #         0,
    #         0,
    #         0,
    #         -10,
    #         10,
    #     )
    # )



# setting up screen
root = tk.Tk()
root.resizable(False, False)
root.title("Anafi Drone GUI")
root.configure(bg='white')

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.configure(bg='white')
canvas.pack()

controlFrame = tk.Frame(root)
controlFrame.configure(bg='white')
controlFrame.place(relwidth=.95, relheight=.95, relx=0.025, rely=0.025)

# # setting up the slider
# var = DoubleVar()
# scale = Scale(controlFrame, variable=var, from_=50, to=-50)
# scale.place(relwidth=0.2, relheight=0.9, relx=0.3, rely=0.05)

# rotate left
l_rotate_button_image = Image.open("images/turn_left.png")
# l_rotate_img = l_rotate_button_image.resize(
#     (ROTATE_BUTTON_WIDTH, ROTATE_BUTTON_HEIGHT), Image.ANTIALIAS)
l_rotate_photoImg = ImageTk.PhotoImage(l_rotate_button_image)
l_rotate_button = Button(controlFrame, image=l_rotate_photoImg, command=turn_left)
l_rotate_button.place(relwidth=.5, relheight=.5, relx=0.1, rely=0.1)

# rotate right
r_rotate_button_image = Image.open("images/turn_right.png")
r_rotate_img = r_rotate_button_image.resize(
    (ROTATE_BUTTON_WIDTH, ROTATE_BUTTON_HEIGHT), Image.ANTIALIAS)
r_rotate_photoImg = ImageTk.PhotoImage(r_rotate_img)
r_rotate_button = Button(
    controlFrame, image=r_rotate_photoImg, command=turn_right)
r_rotate_button.place(relwidth=0.1, relheight=0.8, relx=0.8, rely=0.1)

# takeoff button
takeoff_button = tk.Button(controlFrame, text ="Takeoff", command=takeoff)
takeoff_button.place(relwidth=0.075, relheight=0.1, relx=.3, rely=0.1)

# landing button
landing_button = tk.Button(controlFrame, text ="Land", command=land)
landing_button.place(relwidth=0.075, relheight=0.1, relx=.7, rely=0.1)

# move forward button
forward_button_image = Image.open("images/forward.png")
# forward_button_img = forward_button_image.resize(
#     (ROTATE_BUTTON_WIDTH, ROTATE_BUTTON_HEIGHT), Image.ANTIALIAS)
forward_button_photoImg = ImageTk.PhotoImage(forward_button_image)
forward_button = Button(
    controlFrame, image=forward_button_photoImg, command=move_forward)
forward_button.place(relwidth=0.1, relheight=0.8, relx=0.8, rely=0.1)


# Main Loop Start:

if __name__ == "__main__":
    with olympe.Drone(SPHINX_IP) as drone:
        root.mainloop()