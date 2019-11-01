import serial
from time import sleep

ser = serial.Serial('COM6', 9600)
ser.setDTR(1)
print('COM3 Open', ser.isOpen())

print('Reading...')
while True:
    a = str(ser.readline())
    # print('raw', a)
    # a=a.replace("b'Incoming readings:","")
    # a=a.replace("\\n'","")
    # a = [float(c) for c in a.split("-")]
    print(a)
    sleep(0.1)
# a = None
# while not a:
#     a = ser.readline()
#     sleep(0.1)
# print('Read:', a)
    

# print('Writing...')
# ser.write(b'hello\n')
# print('wrote')
# print('Response', str(ser.readline()))

