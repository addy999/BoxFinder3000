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

def sendRxCommand(ser, motor_command, sleep_req_ms=0.0, offset_s = 0.1):
    
    # Sending
    str_command = commandToStrBytes(motor_command, '-' + str(sleep_req_ms))
    print('Sending', str_command)
    ser.write(str_command)
    
    sleep(sleep_req_ms / 1000 + offset_s) # plus offset to allow comms to come in
    
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
