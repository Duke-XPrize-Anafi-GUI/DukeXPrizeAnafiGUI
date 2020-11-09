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
gimbal_attitude = 0

# Drone constants
DRONE_IP = "192.168.42.1"
SPHINX_IP = "10.202.0.1"

# UI Global variables
HEIGHT = 750
WIDTH = 830
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

# Connect to drone
def connect():
    global is_connected
    if not is_connected:
        drone.connect()
    is_connected = True
    connect_button.config(state = "disabled")
    enable_gimbal_buttons()
    

# Takeoff routine
def takeoff():
    assert drone(TakeOff()).wait().success()
    # Set gimbal to attitude so that it looks straight
    drone(
        gimbal.set_target(
            gimbal_id = 0,
            control_mode = "position",
            yaw_frame_of_reference = "absolute",
            yaw = 0.0,
            pitch_frame_of_reference = "absolute",
            pitch = 0,
            roll_frame_of_reference = "absolute",
            roll = 0.0
        )
    ).wait()
    global gimbal_attitude
    gimbal_attitude = 0.0

    takeoff_button.config(state = "disabled")
    enable_movement_buttons()

# Landing routine
def land():
    assert drone(Landing()).wait().success()
    disable_all_buttons()
    enable_gimbal_buttons()

def move_forward():
    global gimbal_attitude
    
    # Move straight 
    if gimbal_attitude <= 10 and gimbal_attitude >= -10:
        pitch_fwd()
    # Increase throttle - move up
    elif gimbal_attitude == 100:
        increase_throttle()
    # Increase throttle - move down
    elif gimbal_attitude == -100:
        decrease_throttle()
    
def move_gimbal(attitude):
    drone(
        gimbal.set_target(
            gimbal_id = 0,
            control_mode = "position",
            yaw_frame_of_reference = "absolute",
            yaw = 0.0,
            pitch_frame_of_reference = "absolute",
            pitch = attitude,
            roll_frame_of_reference = "absolute",
            roll = 0.0
        )
    ).wait()

def gimbal_up():
    global gimbal_attitude
    new_attitude = gimbal_attitude + 10

    if new_attitude > 100:
        new_attitude = 100

    move_gimbal(new_attitude)

    gimbal_attitude = new_attitude

    if gimbal_attitude != 100:
        takeoff_button.config(state = "disabled")
    else:
        takeoff_button.config(state = "normal")

    land_button.config(state = "disabled")

def gimbal_down():
    global gimbal_attitude
    new_attitude = gimbal_attitude - 10

    if new_attitude < -100:
        new_attitude = -100

    move_gimbal(new_attitude)

    gimbal_attitude = new_attitude
    
    if gimbal_attitude != -100:
        land_button.config(state = "disabled")
    else:
        land_button.config(state = "normal")

    takeoff_button.config(state = "disabled")

def look_forward():
    global gimbal_attitude
    
    move_gimbal(0)

    gimbal_attitude = 0

    takeoff_button.config(state = "disabled")
    land_button.config(state = "disabled")

def look_up():
    global gimbal_attitude

    move_gimbal(100)

    gimbal_attitude = 100

    takeoff_button.config(state = "normal")
    land_button.config(state = "disabled")

def look_down():
    global gimbal_attitude

    move_gimbal(-100)

    gimbal_attitude = -100

    takeoff_button.config(state = "disabled")
    land_button.config(state = "normal")
    
def video_feed():
    p1 = subprocess.Popen(['../clones/parrot-groundsdk/out/pdraw-linux/staging/native-wrapper.sh', 'pdraw', '-u','rtsp://10.202.0.1/live'])

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

# rotate left
l_rotate_button_image = Image.open("images/turn_left.png")
l_rotate_photoImg = ImageTk.PhotoImage(l_rotate_button_image)
l_rotate_button = Button(controlFrame, image=l_rotate_photoImg, command=turn_left)
l_rotate_button.place(relwidth=.2, relheight=.2105, relx=0, rely=0.35)

# rotate right
r_rotate_button_image = Image.open("images/turn_right.png")
r_rotate_photoImg = ImageTk.PhotoImage(r_rotate_button_image)
r_rotate_button = Button(
    controlFrame, image=r_rotate_photoImg, command=turn_right)
r_rotate_button.place(relwidth=.2, relheight=.2105, relx=0.35, rely=0.35)

# move forward button
forward_button_image = Image.open("images/forward.png")
forward_button_photoImg = ImageTk.PhotoImage(forward_button_image)
forward_button = Button(
    controlFrame, image=forward_button_photoImg, command=move_forward)
forward_button.place(relwidth=0.15, relheight=0.1824, relx=0.20, rely=0.1)

# connect button
connect_button_image = Image.open("images/connect.png")
connect_button_photoImg = ImageTk.PhotoImage(connect_button_image)
connect_button = Button(
    controlFrame, image=connect_button_photoImg, command=connect)
connect_button.place(relwidth=0.2, relheight=0.1, relx=0.675, rely=.58)

# takeoff button
takeoff_button_image = Image.open("images/takeoff.png")
takeoff_button_photoImg = ImageTk.PhotoImage(takeoff_button_image)
takeoff_button = Button(
    controlFrame, image=takeoff_button_photoImg, command=takeoff)
takeoff_button.place(relwidth=0.22, relheight=0.28, relx=0.55, rely=.7)

# land button
land_button_image = Image.open("images/land.png")
land_button_photoImg = ImageTk.PhotoImage(land_button_image)
land_button = Button(
    controlFrame, image=land_button_photoImg, command=land)
land_button.place(relwidth=0.22, relheight=0.28, relx=0.785, rely=.7)

# gimbal up button
gimbal_up_button_image = Image.open("images/gimbal_up.png")
gimbal_up_button_photoImg = ImageTk.PhotoImage(gimbal_up_button_image)
gimbal_up_button = Button(
    controlFrame, image=gimbal_up_button_photoImg, command=gimbal_up)
gimbal_up_button.place(relwidth=.207, relheight=.2105, relx=0.56, rely=0.1)

# gimbal down button
gimbal_down_button_image = Image.open("images/gimbal_down.png")
gimbal_down_button_photoImg = ImageTk.PhotoImage(gimbal_down_button_image)
gimbal_down_button = Button(
    controlFrame, image=gimbal_down_button_photoImg, command=gimbal_down)
gimbal_down_button.place(relwidth=.207, relheight=.2105, relx=0.56, rely=0.35)

# look up button
look_up_button_image = Image.open("images/look_up.png")
look_up_button_photoImg = ImageTk.PhotoImage(look_up_button_image)
look_up_button = Button(
    controlFrame, image=look_up_button_photoImg, command=look_up)
look_up_button.place(relwidth=.207, relheight=.15, relx=0.785, rely=0.1)

# look forward button
look_forward_button_image = Image.open("images/look_forward.png")
look_forward_button_photoImg = ImageTk.PhotoImage(look_forward_button_image)
look_forward_button = Button(
    controlFrame, image=look_forward_button_photoImg, command=look_forward)
look_forward_button.place(relwidth=.207, relheight=.15, relx=0.785, rely=0.257)

# look down button
look_down_button_image = Image.open("images/look_down.png")
look_down_button_photoImg = ImageTk.PhotoImage(look_down_button_image)
look_down_button = Button(
    controlFrame, image=look_down_button_photoImg, command=look_down)
look_down_button.place(relwidth=.207, relheight=.15, relx=0.785, rely=0.41)

buttons = [ l_rotate_button, 
            r_rotate_button, 
            forward_button, 
            takeoff_button,
            land_button,
            gimbal_up_button,
            gimbal_down_button,
            look_up_button,
            look_forward_button,
            look_down_button,
            connect_button ]

def disable_all_buttons():
    global buttons
    for button in buttons:
        button.config(state = "disabled")

def enable_all_buttons():
    global buttons
    for button in buttons:
        button.config(state = "normal")

def disable_gimbal_buttons():
    look_up_button.config(state = "disabled")
    look_down_button.config(state = "disabled")
    look_forward_button.config(state = "disabled")
    gimbal_up_button.config(state = "disabled")
    gimbal_down_button.config(state = "disabled")

def enable_gimbal_buttons():
    look_up_button.config(state = "normal")
    look_down_button.config(state = "normal")
    look_forward_button.config(state = "normal")
    gimbal_up_button.config(state = "normal")
    gimbal_down_button.config(state = "normal")

def enable_movement_buttons():
    l_rotate_button.config(state = "normal")
    r_rotate_button.config(state = "normal")
    forward_button.config(state = "normal")

# Main Loop Start:
if __name__ == "__main__":
    with olympe.Drone(SPHINX_IP) as drone:
        disable_all_buttons()
        connect_button.config(state = "normal")
        root.mainloop()
