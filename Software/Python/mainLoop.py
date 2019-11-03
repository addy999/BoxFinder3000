from utilities import *
from motors import *

# Start communicatons
ser = startBT('COM3')

#  Constants
motor_a_coeff = 1.0
motor_b_coeff = 1.0
motor_c_coeff = 1.0
wall_threshold = 5.0 # cm

command = [0.0, 0.0, 0.0] # start by braking

while True:

    ############ Send last made command to robot ############
    sensor_readings = sendRxCommand(ser, command, to_print = True)
    
    ############ Sensor mapping ############
    front_sensor = sensor_readings[0]
    left_sensor = sensor_readings[1]
    right_sensor = sensor_readings[2]
    front_left_sensor = sensor_readings[3]
    front_right_sensor = sensor_readings[4]
    rear_sensor = sensor_readings[5]
    
    ############ Algorithm ############
    
    # 1 - Center rotationally walls
    if front_left_sensor < wall_threshold and front_sensor < wall_threshold * 1.5 and left_sensor < wall_threshold * 1.5:
        # rotate right
        turn(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=1.0, direction=-1)
    
    elif front_right_sensor < wall_threshold and front_sensor < wall_threshold * 1.5 and right_sensor < wall_threshold * 1.5:
        # rotate left
        turn(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=1.0, direction=1)
    
    # 2 - Center btw walls
    elif left_sensor < right_sensor:
        command = slideRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = 1.0)
    elif right_sensor < left_sensor:
        command = slideLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = 1.0)

    # 3 - Check if wall in front
    elif front_sensor < wall_threshold:
        
        if left_sensor < right_sensor:
            # rotate left
            command = turn(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=1.0, direction=1)

        elif right_sensor < left_sensor:
            # rotate right
            command = turn(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=1.0, direction=-1)

        else:
            # Full 180
            command = turn(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=1.0, direction=1)
    
    else:
        command = moveStraight(motor_a_coeff, motor_b_coeff, speed = 1.0, direction = 1)