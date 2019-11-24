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
    
    # # Check if IR can be used
    # if 0.0 < cleaned[6] and reading_map["front-right"] > 27:
    #     print("Using FR IR, would've been", reading_map["front-right"], "now", cleaned[6])
    #     reading_map["front-right"] = cleaned[6]
    # # else:
    # #     print("Using FR-US")
        
    # if 0.0 < cleaned[7]  and reading_map["front-left"] > 27:
    #     print("Using FL IR, would've been", reading_map["front-left"], "now", cleaned[7])
    #     reading_map["front-left"] = cleaned[7]
    # else:
    #     print("Using FL-US")
    
    return reading_map

while not keyboard.is_pressed('esc'):    
    
    if sensor_readings:        
        
        sensor_map = cleanReadings(sensor_readings)
        print(sensor_map)
        
        predict_block = findSquare(direction, sensor_map)
        if predict_block:
            print(predict_block)
        else:
            print("No match found amigo.")
            
        sensor_readings = sendRxCommand(ser, command)
    
    # sleep(0.250)
        
      