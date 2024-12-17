import numpy as np
from adafruit_servokit import ServoKit
import time
from adafruit_servokit import ServoKit
from time import sleep
import threading


# kit.servo[0].angle = 0
# sleep(1)
# kit.servo[0].angle = 30
# Initialize ServoKit for PCA9685 with 16 channels

previous = [0,0,0,0,0]
kit = ServoKit(channels=16)

# Define channel mapping (adjust based on your servo connections)

CHANNEL_BASE = 0
CHANNEL_LINK1 = 1
#CHANNEL_LINK1 =15
CHANNEL_LINK2 = 2
#CHANNEL_LINK2 = 14
CHANNEL_WHIST = 3
CHANNEL_ROTATE = 4

lower_right = 5
lower_left = 6
upper_left  = 7
upper_right = 8
middle = 9
 
#test1 = 15
#test2 = 14
# Define servo angle to PWM pulse conversion function (optional if needed)

def angle_to_pwm(angle):

    # Convert angle (degrees) to PWM duty cycle (assuming 0-270 degrees)

    min_pulse = 500  # Min pulse length out of 4096

    max_pulse = 2500  # Max pulse length out of 4096

    pulse = min_pulse + (max_pulse - min_pulse) * (angle / 270)

    return int(pulse)

def gradual_move(channel, start_angle, end_angle,actuation_range = 270, step=1, delay=0.1):

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

def finger_gripper_close(current):

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

        threading.Thread(target=gradual_move, args=(upper_right, angle_upper_right_max, angle_upper_right_min,180)),

        threading.Thread(target=gradual_move, args=(upper_left, angle_upper_left_max, angle_upper_left_min,180)),        

        threading.Thread(target=gradual_move, args=(middle, angle_midle_max, angle_midle_min,180)),        

        ]

    # Start all threads

    for thread in threads:

        thread.start()

    # Wait for all threads to complete

    for thread in threads:

        thread.join()

def finger_gripper_open(current):

    """ open finger gripper """

    angle_upper_right_max = 0

    angle_upper_right_min = 80


    angle_upper_left_max = 80

    angle_upper_left_min = 0

    angle_midle_max = 80    

    angle_midle_min = 0

    threads = [

        # gradual_move(upper_right, angle_upper_right_min, angle_upper_right_max)

        # gradual_move(upper_left, angle_upper_left_min, angle_upper_left_max)

        # gradual_move(middle, angle_midle_min, angle_midle_max)

        threading.Thread(target=gradual_move, args=(upper_right, angle_upper_right_min, angle_upper_right_max,180)),

        threading.Thread(target=gradual_move, args=(upper_left, angle_upper_left_min, angle_upper_left_max,180)),        

        threading.Thread(target=gradual_move, args=(middle, angle_midle_min, angle_midle_max,180)),        

        ]

    # Start all threads

    for thread in threads:

        thread.start()

    # Wait for all threads to complete

    for thread in threads:

        thread.join()

def control_all_servos_with_threads():

    # Create threads for each servo movement

    threads = [

        threading.Thread(target=move_base, args=(np.deg2rad(0), np.deg2rad(0))),

        threading.Thread(target=move_link1, args=(np.deg2rad(90), np.deg2rad(0))),

        threading.Thread(target=move_link2, args=(np.deg2rad(90), np.deg2rad(0))),

        threading.Thread(target=move_whist, args=(np.deg2rad(90), np.deg2rad(0))),

        # threading.Thread(target=rotate_whist, args=(np.deg2rad(0), np.deg2rad(60))),

    ]

    # Start all threads

    for thread in threads:

        thread.start()

    # Wait for all threads to complete

    for thread in threads:

        thread.join()

    print("All servo movements are completed.")
 
 
    

def fill_control_all_servos_with_threads(previous,goal):
 
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
 

    while True:
        try:
            command = input("\nEnter command (or type 'exit' to quit): ").strip()
            if command.lower() == 'exit':
                print("\nExiting robot loop.\n")
                break

            if command.startswith("goal"):
                try:
                    _, x, y, z, phi = command.split()
                    x, y, z = float(x), float(y), float(z)
                    phi = np.deg2rad(float(phi))  # Convert phi to radians
    
                except ValueError:
                    print("Invalid command format. Use: goal x y z phi\n")

            elif command.startswith("forward"):
                print(f'Base now {previous[0]} ')
                base = float(input("Base (th1) : "))

                print(f'link2 now {previous[1]} ')
                link1 = float(input("link2 (th2) : "))

                print(f'link3 now {previous[2]} ')
                link2 = float(input("link3 (th3) : "))

                print(f'whist now {previous[4]} ')
                whist = float(input("whist (th4) : "))

                goal = (base,link1,link2,whist)


                fill_control_all_servos_with_threads(previous = previous , goal=goal)

                previous = goal

            elif command.startswith("setup"):

                p_base = float(input("Base (th1) : "))
                p_link1 = float(input("link2 (th2) : "))
                p_link2 = float(input("link3 (th3) : "))
                p_whist = float(input("whist (th4) : "))

                previous = (base,link1,link2,whist)
                



        except Exception as e:
            
            print(f"An error occurred: {e}. Waiting for the next command...\n")


#finger_gripper_close(1)
#time.sleep(1)
#finger_gripper_close(0)
#control_all_servos_with_threads()
#move_link2(np.deg2rad(0), np.deg2rad(30))
#move_base(np.deg2rad(-30),np.deg2rad(0))
#rotate_whist(np.deg2rad(-135),np.deg2rad(0))
#gradual_move(CHANNEL_LINK1,135,0)    

 