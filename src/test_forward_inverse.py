import calculation as cal
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

# from matplotlib.animation import FuncAnimation

# # Initialize the figure and 3D axis
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Set axis limits
# ax.set_xlim([-50, 50])
# ax.set_ylim([-50, 50])
# ax.set_zlim([0, 50])

# # Labels
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.set_zlabel("Z")

# # Initialize a line for the robotic arm
# line, = ax.plot([], [], [], 'o-', lw=2)

# # Function to initialize the plot
# def init():
#     line.set_data([], [])
#     line.set_3d_properties([])
#     return line,

# # Update function for the animation
# def update(frame):
#     # Unpack the current joint angles
#     theta1, theta2, theta3, theta4 = frame
#     # Get joint positions using your `joints_plot` function
#     x, y, z = cal.joints_plot(np.rad2deg(theta1), np.rad2deg(theta2), np.rad2deg(theta3), np.rad2deg(theta4))
#     # Update the line data for the animation
#     line.set_data(x, y)
#     line.set_3d_properties(z)
#     return line,
# phi = -60

# phi_loop = True  
# # Prepare the animation steps using `movestep_theta`
# current = []
# goal    = [] 
# while(phi_loop):
#     if not current:
#         current = cal.movej(30, 30, 1, np.deg2rad(phi), True)  # Initial position
#     if not goal:
#         goal = cal.movej(30 , 15 , 1, np.deg2rad(phi), True)  # Target position
#     print(f'tcp eangle {phi} ')
#     if current and goal :
#         print(current,goal)
#         phi_loop = False
#         break
#     elif phi <= -180:
#         break
        
#     phi -= 1
    

# if current and goal:
#     # Generate interpolation for joint angles
#     theta_steps = cal.movestep_theta(current, goal, step=100)  # Adjust step as needed

#     # Combine steps into frames for animation
#     frames = list(zip(*theta_steps))

#     # Create the animation
#     ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=False, interval=100)

#     plt.show()
# else:
#     print("Movement failed or joint limit exceeded.")

print(f"Return {cal.movej(30,30,1)}")
print(f"Return {cal.movej(30,35,1)}")