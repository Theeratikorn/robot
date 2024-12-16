import numpy as np
from adafruit_servokit import ServoKit
import time

# Initialize ServoKit for PCA9685 with 16 channels
kit = ServoKit(channels=16)

# Define channel mapping (adjust based on your servo connections)
CHANNEL_BASE = 0
CHANNEL_LINK1 = 1
CHANNEL_LINK2 = 2
CHANNEL_WHIST = 3
CHANNEL_ROTATE = 4

# Define servo angle to PWM pulse conversion function (optional if needed)
def angle_to_pwm(angle):
    # Convert angle (degrees) to PWM duty cycle (assuming 0-270 degrees)
    min_pulse = 500  # Min pulse length out of 4096
    max_pulse = 2500  # Max pulse length out of 4096
    pulse = min_pulse + (max_pulse - min_pulse) * (angle / 270)
    return int(pulse)

def gradual_move(channel, start_angle, end_angle, step=1, delay=0.02):
    """Move servo gradually from start_angle to end_angle."""
    if start_angle > end_angle:
        step = -step
    for angle in range(int(start_angle), int(end_angle), step):
        kit.servo[channel].angle = angle
        time.sleep(delay)
    # Set final position
    kit.servo[channel].angle = end_angle
    print(f"Channel {channel} moved to angle: {end_angle} degrees")

def move_base(current, th1):
    """Move base servo gradually."""
    angle = np.rad2deg(th1) + 135
    gradual_move(CHANNEL_BASE, current, angle)

def move_link1(current, th2):
    """Move Link1 servo gradually."""
    angle = np.rad2deg(th2)
    gradual_move(CHANNEL_LINK1, current, angle)

def move_link2(current, th3):
    """Move Link2 servo gradually."""
    angle = np.rad2deg(th3) + 135
    gradual_move(CHANNEL_LINK2, current, angle)

def move_whist(current, th4):
    """Move whist servo gradually."""
    angle = np.rad2deg(th4) + 135
    gradual_move(CHANNEL_WHIST, current, angle)

def rotate_whist(current, th5):
    """Rotate whist servo gradually."""
    angle = np.rad2deg(th5) + 135
    gradual_move(CHANNEL_ROTATE, current, angle)

# Example usage
# move_base(0, np.deg2rad(90))
# move_link1(0, np.deg2rad(45))
# move_link2(0, np.deg2rad(60))
# move_whist(0, np.deg2rad(30))
# rotate_whist(0, np.deg2rad(90))
