import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from adafruit_servokit import ServoKit
from time import sleep

# Initialize ServoKit
kit = ServoKit(channels=16)

# Define channel mapping
CHANNEL_BASE = 0
CHANNEL_LINK1 = 1
CHANNEL_LINK2 = 2
CHANNEL_WHIST = 3

# Current and target angles
current_angles = {CHANNEL_BASE: 135, CHANNEL_LINK1: 0, CHANNEL_LINK2: 135, CHANNEL_WHIST: 135}
target_angles = {CHANNEL_BASE: 135, CHANNEL_LINK1: 0, CHANNEL_LINK2: 135, CHANNEL_WHIST: 135}

# Gradual movement function
def gradual_move(channel, start_angle, end_angle, step=1, delay=0.02):
    """Move servo gradually from start_angle to end_angle."""
    if start_angle > end_angle:
        step = -step
    for angle in range(int(start_angle), int(end_angle), step):
        kit.servo[channel].angle = angle
        sleep(delay)
    # Set final position
    kit.servo[channel].angle = end_angle
    print(f"Channel {channel} moved to angle: {end_angle} degrees")

# Update functions for sliders
def update_base(val):
    target_angles[CHANNEL_BASE] = slider_base.val

def update_link1(val):
    target_angles[CHANNEL_LINK1] = slider_link1.val

def update_link2(val):
    target_angles[CHANNEL_LINK2] = slider_link2.val

def update_whist(val):
    target_angles[CHANNEL_WHIST] = slider_whist.val

# Confirmed button callback
def confirmed(event):
    print("\nConfirmed! Moving servos to target positions...\n")
    for channel, target_angle in target_angles.items():
        start_angle = current_angles[channel]
        gradual_move(channel, start_angle, target_angle)
        current_angles[channel] = target_angle

# Create the GUI
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.2, bottom=0.5)

# Slider for Base Servo
ax_slider_base = plt.axes([0.2, 0.4, 0.65, 0.03])
slider_base = Slider(ax_slider_base, 'Base Angle', 0, 270, valinit=target_angles[CHANNEL_BASE])
slider_base.on_changed(update_base)

# Slider for Link1 Servo
ax_slider_link1 = plt.axes([0.2, 0.3, 0.65, 0.03])
slider_link1 = Slider(ax_slider_link1, 'Link1 Angle', 0, 270, valinit=target_angles[CHANNEL_LINK1])
slider_link1.on_changed(update_link1)

# Slider for Link2 Servo
ax_slider_link2 = plt.axes([0.2, 0.2, 0.65, 0.03])
slider_link2 = Slider(ax_slider_link2, 'Link2 Angle', 0, 270, valinit=target_angles[CHANNEL_LINK2])
slider_link2.on_changed(update_link2)

# Slider for Whist Servo
ax_slider_whist = plt.axes([0.2, 0.1, 0.65, 0.03])
slider_whist = Slider(ax_slider_whist, 'Whist Angle', 0, 270, valinit=target_angles[CHANNEL_WHIST])
slider_whist.on_changed(update_whist)

# Add Confirmed Button
ax_button = plt.axes([0.4, 0.02, 0.2, 0.05])
button_confirmed = Button(ax_button, 'Confirmed')
button_confirmed.on_clicked(confirmed)

# Show GUI
plt.show()
