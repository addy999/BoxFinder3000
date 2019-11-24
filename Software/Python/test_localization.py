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
# direction = (0,1)
command = [0, 0, 0, 0, 0]
sensor_readings = None
print('Starting loop...')

def cleanReadings(readings):
    
    # Find mode
    readings = [readings[i*3:i*3+3] for i in range(6)]
    
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
    offsets = [1.5,1.5,1.5,0.5,1.5,1] # when using max(reading)
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
    
    # print("fr", reading_map["front-right"])
    # print("fl", reading_map["front-left"])
    if  reading_map["front-right"] > 12:
        reading_map["front-right"] = 4
    if  reading_map["front-left"] > 12:
        reading_map["front-left"] = 4
    
    return reading_map

readings = []
c = 0

while not keyboard.is_pressed('esc'):    
    
    if sensor_readings:        
        
        sensor_map = cleanReadings(sensor_readings)
        readings.append(sensor_map)
        
        if len(readings) >= 2:
            print(readings[-2])
            print(readings[-1])
            predict_loc, predict_l1, predict_l2 = findSqDirectionMultiReadings(readings[-2], readings[-1])
            print("Facing {0} from {1} to {2}.".format(predict_loc, predict_l1, predict_l2))
            
    sleep(5)
    print("Reading")
    sensor_readings = sendRxCommand(ser, command)