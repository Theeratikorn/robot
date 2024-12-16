import numpy as np
import time
from demo_control_servo import move_base, move_link1, move_link2, move_whist, rotate_whist
from calculation import movej



def servo(theta1, theta2, theta3, theta4,current_theta):
    """Move servos to the target angles gradually."""
    # Assuming the robot starts at 0 degrees for all joints
    current_theta = current_theta
    # Gradually move to target angles
    move_base(current_theta[0], np.deg2rad(theta1))
    move_link1(current_theta[1], np.deg2rad(theta2))
    move_link2(current_theta[2], np.deg2rad(theta3))
    move_whist(current_theta[3], np.deg2rad(theta4))

    current_theta = [theta1, theta2, theta3, theta4]
    return current_theta

def main_loop():
    """Main loop to listen for commands and execute robot movements."""
    print("Robot Command Loop Started. Type 'exit' to quit.")

    current_theta = [0,90,45,90]

    while True:
        command = input("Enter command (format: plan x, y, z, phi): ").strip()

        if command.lower() == "exit":
            print("Exiting command loop.")
            break

        # Parse the command
        try:
            if command.startswith("plan"):
                _, x, y, z, phi = command.split()
                x, y, z, phi = float(x), float(y), float(z), float(phi)

                # Execute movej to get joint angles
                theta1, theta2, theta3, theta4 = movej(x, y, z, phi)

                if None in (theta1, theta2, theta3, theta4):
                    print("Error: Target position is out of reach or violates safety constraints.")
                else:
                    print(f"Moving to position: x={x}, y={y}, z={z}, phi={phi}")
                    print(f"Joint angles: theta1={theta1}, theta2={theta2}, theta3={theta3}, theta4={theta4}")

                    # Call servo function to move the robot
                    current_theta = servo(theta1, theta2, theta3, theta4, current_theta)

            elif command.startswith("Home"):
                theta1, theta2, theta3, theta4 = [0,90,45,90]
                current_theta = servo(theta1, theta2, theta3, theta4, current_theta)  
            else:
                print("Invalid command format. Please use: plan x, y, z, phi")
        except ValueError as e:
            print("Error parsing command. Make sure to use the correct format and numerical values.")
            print(f"Details: {e}")

if __name__ == "__main__":
    main_loop()
