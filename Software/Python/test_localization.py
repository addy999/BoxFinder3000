from utilities import *
from motors import *
import keyboard
from math import cos, radians
from time import sleep
from localization import *

# Start communicatons
ser = startBT('COM6')

# Initialize
direction = (0,1)
command = [0, 0, 0, 0, 0]
sensor_readings = sendRxCommand(ser, command)
print('Starting loop...')

while not keyboard.is_pressed('esc'):    
    
    if sensor_readings:
        
        sensor_readings[1] += 1.5
        # Convert cm to inches
        sensor_readings = [i*0.393 for i in sensor_readings]
    
        sensor_map = {
            'front' : sensor_readings[1] + 1.0,
            'left' : sensor_readings[3] + 1,
            'right' : sensor_readings[4] + 1,
            "front-left" : sensor_readings[0] + 0.0,
            "front-right" : sensor_readings[2] + 0.5,
            'back' : sensor_readings[5] + 0.5,
        }        
        
        print(sensor_map)
        
        predict_block = findSquare(direction, sensor_map)
        if predict_block:
            print(predict_block)
        else:
            print("No match found amigo.")
            
        sensor_readings = sendRxCommand(ser, command)
    
    # sleep(0.250)
        
      