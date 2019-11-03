import serial
from time import sleep

def startBT(port):

    ser = serial.Serial(port, 9600)
    ser.setDTR(1)
    print(ser.name, 'Open: ', ser.isOpen())
    return ser

def commandToStr(command = list):
    
    str_list = ''.join(str(e) for e in command)
    str_list += "\n"
    return bytes(str_list, 'utf-8')

def sendRxCommand(ser, command, to_print=False):
    if to_print:
        print('Sending')
    ser.write(commandToStr(command));
    
    sleep(0.1)
    
    if to_print:
        print('Reading...')
    a = str(ser.readline())
    if len(a) > 20:
        a = a[2:-2]
        a = a.replace("\\","")
        a = a.replace("\n", "")
        a = a.replace("  ", "")[:-1]
        a = [float(c) for c in a.split("-")]
        print(a)
        return a

# print('Writing...')
# ser.write(b'hello\n')
# print('wrote')
# print('Response', str(ser.readline()))

