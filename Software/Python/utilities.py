import serial
from time import sleep

def startBT(port):

    ser = serial.Serial(port, 9600)
    ser.setDTR(1)
    print(ser.name, 'Open: ', ser.isOpen())
    return ser

def commandToStrBytes(command = list, to_add = ""):
    
    str_list = ','.join(str(e) for e in command)
    str_list += to_add
    str_list += "\n"
    return bytes(str_list, 'utf-8')

def allowReadingsDiff(current, last, multiple = 2):
    
    i =0 
    
    for c,l in zip(current, last):
        if i in [0,2]: pass
        else:
            if l > 0:
                if c/l >= multiple:
                    return False
            if c > 0:
                if l/c >= multiple:
                    return False
            
    return True
