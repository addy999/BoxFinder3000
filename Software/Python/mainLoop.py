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
motor_c_coeff = 0.7

front_threshold = 12 # cm
side_threshold = 4 # cm
# diagonal_threshhold = 11
diagonal_threshhold = side_threshold / cos(radians(45)) + 1.5
turn_threshold = 15 # cm

speed = 0.8
turn_speed = 0.96
straighten_speed = 45/120
slide_speed = 0.6

base_turn_time_ms = 4200/2 * 2/3
ninty_deg_turn_time_ms = 1.85 * base_turn_time_ms/3 
pi_rad_turn_time_ms = 1.8 * base_turn_time_ms*2/3
slide_time_ms = 0.75 * ninty_deg_turn_time_ms / 3
reverse_time_ms = 200
straighten_time = 0.25 * 4200/2 * 2/3

const_loop_delay_ms = 200 # ms

# Initialize
command = [0, 0, 0]
sensor_readings = sendRxCommand(ser, command)
last_readings = sensor_readings
multiple_allowed = 1.5

print('Starting loop...')

skip_loop = False

while not keyboard.is_pressed('esc'):    
    
    if sensor_readings and not skip_loop:
    
        # Zero out sleep at beginning
        sleep_req_ms = 0.0 # ms
        skip_loop = False
        
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
                    
            # 2b - Check which side to rotate
            if sensor_map['left_sensor'] < sensor_map['right_sensor']:
                print('> turn right')
                command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
                sleep_req_ms = ninty_deg_turn_time_ms
            else:
                print('> turn left')
                command = turnLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
                sleep_req_ms = ninty_deg_turn_time_ms

            # elif sensor_map['right_sensor'] < sensor_map['left_sensor'] and sensor_map['right_sensor'] < turn_threshold:
            #     print('> turn left')
            #     command = turnLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
            #     sleep_req_ms = ninty_deg_turn_time_ms

            # else:
            #     print('> 180')
            #     command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
            #     sleep_req_ms = pi_rad_turn_time_ms
                 
        # 3 - Center btw walls
        elif sensor_map['left_sensor'] < sensor_map['right_sensor'] and (sensor_map['left_sensor'] < side_threshold or sensor_map['front_left_sensor'] < diagonal_threshhold):
            print('> slide right')
            command = slideRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = slide_speed)
            sleep_req_ms = slide_time_ms
        elif sensor_map['right_sensor'] < sensor_map['left_sensor'] and (sensor_map['right_sensor'] < side_threshold or sensor_map['front_right_sensor'] < diagonal_threshhold):
            print('> slide left')
            command = slideLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = slide_speed)
            sleep_req_ms = slide_time_ms
        
        # 2 - Straighten out
        # elif sensor_map['front_left_sensor'] < diagonal_threshhold:
        #     print('> Rotate right')
        #     command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = straighten_speed)               
        #     sleep_req_ms = straighten_time
            
        # elif sensor_map['front_right_sensor'] < diagonal_threshhold:
            
        #     print('> Rotate Left')
        #     command = turnLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = straighten_speed)  
        #     sleep_req_ms = straighten_time
            
        # 4 - Else, just go forward
        else:
            print('> forward')
            command = moveFwd(motor_a_coeff, motor_b_coeff, speed = speed)
            sleep_req_ms = const_loop_delay_ms
        
        # 5 - Send commands
        # print('Command', command)
        print('Read', sensor_map.items())        
        last_readings = sensor_readings
        sensor_readings = sendRxCommand(ser, command, sleep_req_ms = sleep_req_ms, offset_s = 0.0)
        # skip_loop = not allowReadingsDiff(sensor_readings, last_readings, 1.5)
        if last_readings[1] > 0 and sensor_readings[1] > 0:
            if last_readings[1] / sensor_readings[1] >= multiple_allowed:
                skip_loop = True
        # sleep(const_loop_delay_ms / 1000)
    else:
        if skip_loop: print('SKIPPING LOOP')
        print('******************** Give last command ********************')
        print('Read', sensor_map.items())        
        sensor_readings = sendRxCommand(ser, [0.0, 0.0, 0.0], sleep_req_ms = sleep_req_ms, offset_s = 0.0)
        last_readings = sensor_readings
        skip_loop = False
# Break and end
sendRxCommand(ser, [0, 0, 0])