import numpy as np

from adafruit_servokit import ServoKit

import time
from adafruit_servokit import ServoKit
from time import sleep
import threading
 

from adafruit_servokit import ServoKit

from time import sleep

import threading


# kit.servo[0].angle = 0

# sleep(1)

# kit.servo[0].angle = 30

# Initialize ServoKit for PCA9685 with 16 channels

kit = ServoKit(channels=16)

# Define channel mapping (adjust based on your servo connections)

CHANNEL_BASE = 0

CHANNEL_LINK1 = 1

#CHANNEL_LINK1 =15

CHANNEL_LINK2 = 2

#CHANNEL_LINK2 = 14

CHANNEL_WHIST = 3

CHANNEL_ROTATE = 4

lower_right = 4

lower_left = 5

upper_left  = 6

upper_right = 7

middle = 8
 
#test1 = 15

#test2 = 14


# Define servo angle to PWM pulse conversion function (optional if needed)

def angle_to_pwm(angle):

    # Convert angle (degrees) to PWM duty cycle (assuming 0-270 degrees)

    min_pulse = 500  # Min pulse length out of 4096

    max_pulse = 2500  # Max pulse length out of 4096

    pulse = min_pulse + (max_pulse - min_pulse) * (angle / 270)
    return int(pulse)

def gradual_move(channel, start_angle, end_angle,actuation_range = 270, step=1, delay=0.02):

    """Move servo gradually from start_angle to end_angle."""

    min_pulse = 500  # Min pulse length out of 4096

    max_pulse = 2500  # Max pulse length out of 4096

    print("gradual_move")

    kit.servo[channel].actuation_range = actuation_range

    kit.servo[channel].set_pulse_width_range(500, 2500)

    print(f"start {start_angle} stop {end_angle}")

    if start_angle > end_angle:

        step = -step

    for angle in range(int(start_angle), int(end_angle), step):

        kit.servo[channel].angle = angle

        print(f"servo {channel} angle {angle} deg")

        time.sleep(delay)



def move_base(current, th1):

    """Move base servo gradually."""

    angle = np.rad2deg(th1) + 135

    current = np.rad2deg(current) + 135

    gradual_move(CHANNEL_BASE, current, angle)

def move_link1(current, th2):

    """Move Link1 servo gradually."""

    angle = np.rad2deg(th2)

    current = np.rad2deg(current)

    gradual_move(CHANNEL_LINK1, current, angle)

    print("movelink1")

def move_link2(current, th3):

    """Move Link2 servo gradually."""

    angle = np.rad2deg(th3) + 135

    current = np.rad2deg(current) + 135

    gradual_move(CHANNEL_LINK2, current, angle)

    print("movelink2")

def move_whist(current, th4):

    """Move whist servo gradually."""

    angle = -np.rad2deg(th4) + 135

    current = -np.rad2deg(current) + 135    

    gradual_move(CHANNEL_WHIST, current, angle)

def rotate_whist(current, th5):

    """Rotate whist servo gradually."""

    angle = np.rad2deg(th5) + 135

    current = np.rad2deg(current) + 135

    gradual_move(CHANNEL_ROTATE, current, angle)

def finger_gripper_close():

    """close finger gripper"""

    angle_upper_right_max = 0
    angle_upper_right_min = 80


    angle_upper_left_max = 80

    angle_upper_left_min = 0

    angle_midle_max = 80    

    angle_midle_min = 0

    # gradual_move(upper_right, angle_upper_right_max, angle_upper_right_min)

    # gradual_move(upper_left, angle_upper_left_max, angle_upper_left_min)

    # gradual_move(middle, angle_midle_max, angle_midle_min)

    threads = [

        threading.Thread(target=gradual_move, args=(upper_right, angle_upper_right_max, angle_upper_right_min)),

        threading.Thread(target=gradual_move, args=(upper_left, angle_upper_left_max, angle_upper_left_min)),        

        threading.Thread(target=gradual_move, args=(middle, angle_midle_max, angle_midle_min)),        

        ]

    # Start all threads

    for thread in threads:

        thread.start()

    # Wait for all threads to complete

    for thread in threads:

        thread.join()

def finger_gripper_open():

    """ open finger gripper """

    angle_upper_right_max = 0
    angle_upper_right_min = 80


    angle_upper_left_max = 80

    angle_upper_left_min = 0

    angle_midle_max = 80    

    angle_midle_min = 0

    threads = [

        threading.Thread(target=gradual_move, args=(upper_right, angle_upper_right_min, angle_upper_right_max)),

        threading.Thread(target=gradual_move, args=(upper_left, angle_upper_left_min, angle_upper_left_max)),        

        threading.Thread(target=gradual_move, args=(middle, angle_midle_min, angle_midle_max)),        

        ]

    # Start all threads

    for thread in threads:

        thread.start()

    # Wait for all threads to complete

    for thread in threads:

        thread.join()

def control_all_servos_with_threads(previous,goal):

    # Create threads for each servo movement
    p_th1 , p_th2 , p_th3 , p_th4 = previous
    th1 , th2 , th3 , th4 = goal

    threads = [

        threading.Thread(target=move_base, args=(np.deg2rad(p_th1), np.deg2rad(th1))),

        threading.Thread(target=move_link1, args=(np.deg2rad(p_th2), np.deg2rad(th2))),

        threading.Thread(target=move_link2, args=(np.deg2rad(p_th3), np.deg2rad(th3))),

        threading.Thread(target=move_whist, args=(np.deg2rad(p_th4), np.deg2rad(th4))),

    ]

    # Start all threads

    for thread in threads:

        thread.start()

    # Wait for all threads to complete

    for thread in threads:

        thread.join()

    print("All servo movements are completed.")

 
