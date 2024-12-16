import numpy as np
import time

# Simulating channel mapping for servos
CHANNEL_BASE = 0
CHANNEL_LINK1 = 1
CHANNEL_LINK2 = 2
CHANNEL_WHIST = 3
CHANNEL_ROTATE = 4

# Simulating gradual servo movement
def gradual_move(channel, start_angle, end_angle, step=1, delay=0.02):
    """Simulate servo gradually moving from start_angle to end_angle."""
    if start_angle > end_angle:
        step = -step
    print(f"Moving channel {channel} from {start_angle:.2f} to {end_angle:.2f}")
    for angle in np.arange(start_angle, end_angle, step):
        print(f"Channel {channel}: {angle:.2f}")
        time.sleep(delay)
    print(f"Channel {channel} reached {end_angle:.2f}\n")

# Base servo control
def move_base(current, th1):
    """Simulate base servo gradually moving."""
    angle = np.rad2deg(th1) + 135
    current = current  + 135
    gradual_move(CHANNEL_BASE, current, angle)

# Link1 servo control
def move_link1(current, th2):
    """Simulate Link1 servo gradually moving."""
    angle = np.rad2deg(th2)
    current = current  + 0
    gradual_move(CHANNEL_LINK1, current, angle)

# Link2 servo control
def move_link2(current, th3):
    """Simulate Link2 servo gradually moving."""
    angle = np.rad2deg(th3) + 135
    current = current  + 135
    gradual_move(CHANNEL_LINK2, current, angle)

# Whist servo control
def move_whist(current, th4):
    """Simulate Whist servo gradually moving."""
    angle = np.rad2deg(th4) + 135
    current = current  + 135
    gradual_move(CHANNEL_WHIST, current, angle)

# Rotate servo control (Optional for future expansion)
def rotate_whist(current, th5):
    """Simulate Whist rotation servo gradually moving."""
    angle = np.rad2deg(th5) + 135
    current = current  + 135
    gradual_move(CHANNEL_ROTATE, current, angle)

# # Example usage (demo mode)
# if __name__ == "__main__":
#     print("Demo: Simulating servo movements")
#     move_base(0, np.deg2rad(45))
#     move_link1(0, np.deg2rad(30))
#     move_link2(0, np.deg2rad(-15))
#     move_whist(0, np.deg2rad(60))
#     rotate_whist(0, np.deg2rad(90))
