import serial
from time import sleep

ser = serial.Serial('COM6', 9600)
ser.setDTR(1)
print(ser.name, 'Open: ', ser.isOpen())

# print('writing...')
# ser.write(b'-255,-255,-255\n')
# sleep(3)
# print('change dir')
# ser.write(b'255,255,255\n')
# sleep(3)
# print('brake')
# ser.write(b'0,0,0\n')

def sendCommand(last_command):
    print('Sending')
    ser.write(last_command);
    
    sleep(0.1)
    
    print('Reading...')
    a = str(ser.readline())
    if len(a) > 20:
        a = a[2:-2]
        a = a.replace("\\","")
        a = a.replace("\n", "")
        a = a.replace("  ", "")[:-1]
        a = [float(c) for c in a.split("-")]
        print(a)

print('FORWARD')
for i in range(10):
    last_command = b'255,255,255\n'
    sendCommand(last_command)

print('BACKWARD')
for i in range(10):
    last_command = b'-255,-255,-255\n'
    sendCommand(last_command)
    
    
        
    
    

# print('Writing...')
# ser.write(b'hello\n')
# print('wrote')
# print('Response', str(ser.readline()))

