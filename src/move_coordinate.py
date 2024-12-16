import time
import sys
import numpy as np
import calculation as cal  # Importing the user-provided module
import demo_control_servo as servo  # Importing the servo library (renamed file to servo_control)
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Wrapper for movej function using the user's module
def move(x, y, z, phi):
    print(f"\nPlanning move to: x={x}, y={y}, z={z}, phi={phi}\n")
    result = cal.movej(x, y, z, phi)  # phi already converted to radians in robot_loop
    if result:
        # Convert result from degrees to radians
        result_rad = [np.deg2rad(angle) for angle in result]
        print(f"Calculated joint angles (radians): {result_rad}\n")
        return result_rad
    else:
        print("Movej failed due to invalid joint angles.\n")
        return None

def perform_servo_movement(joint_angles, current):
    """Perform servo movements based on joint angles."""
    th1, th2, th3, th4 = joint_angles
    print(f"\nPerforming servo movements:")
    print(f"Base: {np.rad2deg(th1)}, Link1: {np.rad2deg(th2)}, Link2: {np.rad2deg(th3)}, Whist: {np.rad2deg(th4)}\n")
    
    # Move each servo with gradual movement
    servo.move_base(current[0], th1)
    servo.move_link1(current[1], th2)
    servo.move_link2(current[2], th3)
    servo.move_whist(current[3], th4)

    print("Servo movements completed.\n")

def joints_plot(theta1, theta2, theta3, theta4):
    print(f"\nPlotting joints with angles: {theta1}, {theta2}, {theta3}, {theta4}\n")
    x, y, z = cal.joints_plot(theta1, theta2, theta3, theta4)
    print(f"Joint positions: x={x}, y={y}, z={z}\n")
    return x, y, z

def movestep_theta(current_rad_theta, goal_rad_theta, step=100):
    print(f"\nGenerating steps from {current_rad_theta} to {goal_rad_theta} with {step} steps\n")
    steps = cal.movestep_theta(current_rad_theta, goal_rad_theta, step)
    if not steps:
        print("No steps generated. Check the movestep_theta function.\n")
    return steps

def forward_kinematics_control(current):
    """Interactive forward kinematics control using sliders."""
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.4)

    # Define sliders for each joint
    ax_base = plt.axes([0.25, 0.3, 0.65, 0.03])
    ax_link1 = plt.axes([0.25, 0.25, 0.65, 0.03])
    ax_link2 = plt.axes([0.25, 0.2, 0.65, 0.03])
    ax_whist = plt.axes([0.25, 0.15, 0.65, 0.03])

    slider_base = Slider(ax_base, 'Base', -135, 135, valinit=current[0])
    slider_link1 = Slider(ax_link1, 'Link1', 0, 135, valinit=current[1])
    slider_link2 = Slider(ax_link2, 'Link2', -135, 135, valinit=current[2])
    slider_whist = Slider(ax_whist, 'Whist', -135, 135, valinit=current[3])

    # Buttons for confirm and exit
    ax_confirm = plt.axes([0.8, 0.05, 0.1, 0.04])
    button_confirm = Button(ax_confirm, 'Confirm')

    ax_exit = plt.axes([0.6, 0.05, 0.1, 0.04])
    button_exit = Button(ax_exit, 'Exit')

    def update_servo(val):
        base_angle = np.deg2rad(slider_base.val)
        link1_angle = np.deg2rad(slider_link1.val)
        link2_angle = np.deg2rad(slider_link2.val)
        whist_angle = np.deg2rad(slider_whist.val)
        print(f"\nSlider updated angles (deg): Base: {slider_base.val}, Link1: {slider_link1.val}, Link2: {slider_link2.val}, Whist: {slider_whist.val}\n")
        return base_angle, link1_angle, link2_angle, whist_angle

    def on_confirm(event):
        base, link1, link2, whist = update_servo(None)
        perform_servo_movement([base, link1, link2, whist], current)
        print("Servo movements confirmed.\n")

    def on_exit(event):
        print("Exiting forward kinematics control.\n")
        plt.close(fig)

    button_confirm.on_clicked(on_confirm)
    button_exit.on_clicked(on_exit)

    plt.show()
    return current

def robot_loop():
    current = [0, 90, 45, -90]  # Initialize current joint angles in degrees

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

                    goal = move(x, y, z, phi)  # Compute goal joint angles

                    if goal is None:
                        print("Goal joint angles are None. Waiting for the next command...\n")
                        continue

                    # Convert to radians before processing
                    current_rad = [np.deg2rad(angle) for angle in current]
                    goal_rad = [np.deg2rad(angle) for angle in goal]
                    print(f"Current joint angles (radians): {current_rad}\n")
                    print(f"Goal joint angles (radians): {goal_rad}\n")

                    # Simulate step calculation without visualization
                    steps = movestep_theta(current_rad, goal_rad, step=100)
                    if steps:
                        print("Steps calculated successfully.\n")
                    else:
                        print("Failed to calculate steps.\n")

                    # Perform servo movements
                    perform_servo_movement(goal_rad, current)

                except ValueError:
                    print("Invalid command format. Use: goal x y z phi\n")

            elif command == "forward":
                current = forward_kinematics_control(current)

            else:
                print("Unknown command. Use: goal x y z phi or forward\n")
        except Exception as e:
            print(f"An error occurred: {e}. Waiting for the next command...\n")

# Run the robot control loop
if __name__ == "__main__":
    robot_loop()
