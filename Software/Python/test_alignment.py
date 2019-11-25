from utilities import *
from robot import *

# Start communications
ser = startBT('COM6')

robot = Robot(
    debug = False,
    ser = ser,
    open_threshold = 12,
    open_angle = 60.0,
    close_angle = 5,
    block_threshold = 4.5,
    
    speed = 0.8,
    turn_speed = 0.96,
    straighten_speed = 45/120,
    slide_speed = 1,
    
    front_threshold = 13 * 0.393,
    side_threshold = 4 * 0.393 ,
    # diagonal_threshhold = 11,
    # diagonal_threshhold = 4 * 0.393 / cos(radians(45)) + 1.5* 0.393,
    
    ninty_deg_turn_time_ms = 1.65 * 4200/2 * 2/3/3,
    slide_time_ms = 0.75 * 1.65 * 4200/2 * 2/3/3 / 3,
    reverse_time_ms = 100,
    straighten_time = 0.25 * 4200/2 * 2/3,
    forward_time_ms = 150, # ms
)

robot.location = (5,0)
robot.pickUpBlock()