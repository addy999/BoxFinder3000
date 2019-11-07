from utilities import *
from motors import *
# from mainLoop import *

ser = startBT('COM6')
sendRxCommand(ser, [0,0,0])

while True:
    command = turnRight()    
    sendRxCommand(ser, command)
    
    # sendRxCommand(ser, [255,255,255])
    # sendRxCommand(ser, turnRight(), 300)

# print('FORWARD')
# for i in range(10):
#     last_command = b'255,255,255\n'
#     sendCommand(ser, last_command)

# print('BACKWARD')
# for i in range(10):
#     last_command = b'-255,-255,-255\n'
#     sendCommand(ser, last_command)