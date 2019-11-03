from utilities import *
from motors import *

ser = startBT('COM3')

print('Always forward')
while True:
    sendRxCommand(ser, [255,255,255], True)

# print('FORWARD')
# for i in range(10):
#     last_command = b'255,255,255\n'
#     sendCommand(ser, last_command)

# print('BACKWARD')
# for i in range(10):
#     last_command = b'-255,-255,-255\n'
#     sendCommand(ser, last_command)