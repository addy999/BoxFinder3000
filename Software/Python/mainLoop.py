from utilities import *
from motors import *
import keyboard
from math import cos, radians
from time import sleep

# Start communicatons
ser = startBT('COM6')

#  Constants
motor_a_coeff = 0.95
motor_b_coeff = 1.0
motor_c_coeff = 1.0

front_threshold = 20 # cm
side_threshold = 3 # cm
diagonal_threshhold = 1.5 * side_threshold  / cos(radians(45))
turn_threshold = 15 # cm

speed = 0.8
turn_speed = 0.96
straighten_speed = 45/180
slide_speed = 0.5

base_turn_time_ms = 4200/2 * 2/3
ninty_deg_turn_time_ms = base_turn_time_ms/3 
pi_rad_turn_time_ms = base_turn_time_ms*2/3
reverse_time_ms = 200
straighten_time = 0.25 * 4200/2 * 2/3

const_loop_delay_ms = 300 # ms

# Initialize
sensor_readings = sendRxCommand(ser, [0, 0, 0])
print('Starting loop...')

while not keyboard.is_pressed('esc'):    
    
    if sensor_readings:
    
        # Zero out sleep at beginning
        sleep_req_ms = 0.0 # ms
        
        ############ Sensor mapping ############
        sensor_map = dict(
            front_sensor = sensor_readings[1],
            left_sensor = sensor_readings[3],
            right_sensor = sensor_readings[4],
            front_left_sensor = sensor_readings[0],
            front_right_sensor = sensor_readings[2],
            # rear_sensor = sensor_readings[5]
        )        
        
        # 1 - Check if wall in front
        if sensor_map['front_sensor'] < front_threshold:
            
            # 2a - Reverse
            if sensor_map['front_sensor'] < front_threshold * 2/3:
                command = moveBwd(motor_a_coeff, motor_b_coeff, speed=speed)
                sleep_req_ms = reverse_time_ms
            
            # 2b - Check which side to rotate
            elif sensor_map['left_sensor'] < sensor_map['right_sensor'] and sensor_map['left_sensor'] < turn_threshold:
                print('> turn right')
                command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
                sleep_req_ms = ninty_deg_turn_time_ms

            elif sensor_map['right_sensor'] < sensor_map['left_sensor'] and sensor_map['right_sensor'] < turn_threshold:
                print('> turn left')
                command = turnLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
                sleep_req_ms = ninty_deg_turn_time_ms

            else:
                print('> 180')
                command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
                sleep_req_ms = pi_rad_turn_time_ms
        
        # 2 - Straighten out
        elif sensor_map['front_left_sensor'] < sensor_map['front_right_sensor'] and sensor_map['front_left_sensor'] < sensor_map['left_sensor'] and sensor_map['front_left_sensor'] < diagonal_threshhold:
            print('> Rotate Left')
            command = turnLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = straighten_speed)  
            sleep_req_ms = straighten_time
            
        elif sensor_map['front_right_sensor'] < sensor_map['front_left_sensor'] and sensor_map['front_right_sensor'] < sensor_map['right_sensor'] and sensor_map['front_right_sensor'] < diagonal_threshhold:
            print('> Rotate right')
            command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = straighten_speed)               
            sleep_req_ms = straighten_time
         
        # 3 - Center btw walls
        elif sensor_map['left_sensor'] < sensor_map['right_sensor'] and sensor_map['left_sensor'] < side_threshold:
            print('> slide right')
            command = slideRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = slide_speed)
        elif sensor_map['right_sensor'] < sensor_map['left_sensor'] and sensor_map['right_sensor'] < side_threshold:
            print('> slide left')
            command = slideLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = slide_speed)
        
        # 4 - Else, just go forward
        else:
            print('> forward')
            command = moveFwd(motor_a_coeff, motor_b_coeff, speed = speed)
        
        # 5 - Send commands
        # print('Command', command)
        # print('Read', sensor_map.items())        
        sensor_readings = sendRxCommand(ser, command, sleep_req_ms = sleep_req_ms + const_loop_delay_ms, offset_s = 0.0)
        # sleep(const_loop_delay_ms / 1000)
        
# Break and end
sendRxCommand(ser, [0, 0, 0])