from utilities import *
from motors import *
import keyboard
from math import cos, radians
from time import sleep
from localization import *
from scipy import stats

# Start communicatons
ser = startBT('COM6')

# Initialize
direction = (0,1)
command = [0, 0, 0, 0, 0]
sensor_readings = sendRxCommand(ser, command)
print('Starting loop...')

#  Constants
motor_a_coeff = 0.955
motor_b_coeff = 1.0
motor_c_coeff = 0.725

speed = 0.8
turn_speed = 0.96
straighten_speed = 45/120
slide_speed = 0.6

front_threshold = 12 * 0.393
side_threshold = 4 * 0.393
# diagonal_threshhold = 11
diagonal_threshhold = side_threshold / cos(radians(45)) + 1.5* 0.393
turn_threshold = 15* 0.393

base_turn_time_ms = 4200/2 * 2/3
ninty_deg_turn_time_ms = 1.65 * base_turn_time_ms/3 
# pi_rad_turn_time_ms = 1.8 * base_turn_time_ms*2/3
slide_time_ms = 0.75 * ninty_deg_turn_time_ms / 3
reverse_time_ms = 100
straighten_time = 0.25 * 4200/2 * 2/3
forward_time_ms = 150 # ms

aligned = False
        
def cleanReadings(readings):
    
    # Find mode
    readings = [readings[i*3:i*3+3] for i in range(8)]
    
    cleaned = []
    for reading in readings:
        reading = [int(i) for i in reading]
        # cleaned.append(max(reading))
        cleaned.append(sum(reading) / len(reading))
        # cleaned.append(int(stats.mode(reading)[0]))
    
    # To inches
    cleaned = [i*0.393 for i in cleaned]
    
    # Add offsets in inches
    # f-l, f, f-r, l, r, b, ir-f-r, ir-f-l
    offsets = [1.5,1.5,1.5,0.5,1.5,1, 0.0, 0.0] # when using max(reading)
    cleaned = [cleaned[i] + offsets[i] for i in range(len(offsets))]
    
    # Round
    cleaned = [round(i, 1) for i in cleaned]
    
    reading_map = {
            'front' : cleaned[1],
            'left' : cleaned[3],
            'right' : cleaned[4],
            "front-left" : cleaned[0],
            "front-right" : cleaned[2],
            'back' : cleaned[5],
        }     
    
    if  reading_map["front-right"] > 12:
        reading_map["front-right"] = 4
    if  reading_map["front-left"] > 12:
        reading_map["front-left"] = 4
    
    return reading_map

while not aligned:    
    
    if sensor_readings:        
        
        sensor_map = cleanReadings(sensor_readings)
        
        # 1 - Check if aligned
        good_count = 0        
        for sensor in sensor_map:
            if "-" not in sensor:
                if sensor_map[sensor] <= 3:
                    good_count += 1
        if good_count >= 2:
            aligned = True   
        
        # 2 - Center btw walls
        if sensor_map['left'] < sensor_map['right'] and (sensor_map['left'] < side_threshold or sensor_map['front-left'] < diagonal_threshhold):
            print('> slide right')
            command = slideRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = slide_speed)
            sleep_req_ms = slide_time_ms
        elif sensor_map['right'] < sensor_map['left'] and (sensor_map['right'] < side_threshold or sensor_map['front-right'] < diagonal_threshhold):
            print('> slide left')
            command = slideLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed = slide_speed)
            sleep_req_ms = slide_time_ms
        elif sensor_map['front'] < front_threshold * 0.35:
            print('> Reverse')
            command = moveBwd(motor_a_coeff, motor_b_coeff, speed)
            sleep_req_ms = reverse_time_ms        
        elif not aligned:
            print('> turn right')
            command = turnRight(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed=turn_speed)
            sleep_req_ms = ninty_deg_turn_time_ms * 0.25
            
        command.append(0.0) # angle
        command.append(sleep_req_ms)
        sensor_readings = sendRxCommand(ser, command)
    
    # sleep(0.250)

print("ALIGNED BITCH")
        
      