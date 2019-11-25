from utilities import *
from motors import *
# from mainLoop import *

def sendRxCommand(ser, command, offset_s = 0.1):
            
        # Sending
        str_command = commandToStrBytes(command)
        # print('Sending', str_command)
        ser.write(str_command)
        
        sleep(command[-1]/1000 + offset_s) 
        # plus offset to allow comms to come in
        
        # Reading
        a = str(ser.readline())
        if len(a) > 20:
            a = a[2:-2]
            a = a.replace("\\","")
            a = a.replace("\n", "")
            a = a.replace("  ", "")[:-1]
            a = [float(c) for c in a.split("-")]
            return a
        else:
            return None
           
ser = startBT('COM6')
while True:
    print(sendRxCommand(ser, [0,0,0,0,200]))
    # sendRxCommand(ser, [10,10,10,5,200])

# while True:
    

# print('BACKWARD')
# for i in range(10):
#     last_command = b'-255,-255,-255\n'
#     sendCommand(ser, last_command)