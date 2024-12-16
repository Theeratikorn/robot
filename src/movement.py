import numpy as np
import control_servo as servo
# for movement robot 

def Home(current):
    th1_c,th2_c,th3_c,th4_c = current # th_c = theta current
    servo.move_whist(th4_c,-80)
    servo.move_link2(th3_c,45)
    servo.move_link1(th2_c,90)
    servo.move_base(th1_c,0)

    
    print()