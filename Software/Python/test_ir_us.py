from utilities import *
from motors import *

ser = startBT('COM6')

while True:
    a = str(ser.readline())
    if a:
        print(a)