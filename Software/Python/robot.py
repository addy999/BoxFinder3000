from utilities import *
from motors import *
import keyboard
from math import cos, radians
from time import sleep
from localization import *
from scipy import stats
import time

class Readings:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Robot:
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        self.readings = []
        self.last_reading = None
        self.last_angle = 0.0
        self.last_motor_commands = [0,0,0]
        self.last_sleep = 0.0
        self.init_localization_done = False
        self.location = None
        self.facing = None
        self.brake()
        
        self.policy_loading_zone = {
                (0,0) : "up",
                (0,1) : "right",
                (0,2) : "down",
                (0,3) : "down",
                (1,1) : "right",
                (2,0) : "up",
                (2,1) : "right",
                (2,2) : "down",
                (2,3) : "right",
                (3,1) : "right",
                (3,3) : "right",
                (4,0) : "right",
                (4,1) : "down",
                (4,3) : "right",
                (5,0) : "right",
                (5,2) : "up",
                (5,3) : "right",
                (6,3) : "right",
                (7,2) : "down",
                (7,3) : "down",
        }
        
        self.policy_to_B_5_2 = {
                (5,3) : "down",
                (6,0) : "right",
                (6,1) : "right",
                (6,3) : "left",
                (7,0) : "up",
                (7,1) : "up",
                (7,2) : "up",
                (7,3) : "left",
        }
        
        self.policy_to_B_2_0 = {
                (2,1) : "down",
                (3,1) : "left",
                (4,0) : "up",
                (4,1) : "left",
                (5,0) : "left",
                (6,0) : "left",
                (6,1) : "down",
                (7,0) : "left",
                (7,1) : "down",
        }

        self.policy_to_B_0_0 = {
                (0,1) : "down",
                (1,1) : "left",
                (2,1) : "left",
                (3,1) : "left",
                (4,0) : "up",
                (4,1) : "left",
                (5,0) : "left",
                (6,0) : "left",
                (6,1) : "down",
                (7,0) : "left",
                (7,1) : "down",
        }
        
        self.policy_to_B_0_3 = {
                (0,1) : "up",
                (0,2) : "up",
                (1,1) : "left",
                (2,1) : "left",
                (3,1) : "left",
                (4,0) : "up",
                (4,1) : "left",
                (5,0) : "left",
                (6,0) : "left",
                (6,1) : "down",
                (7,0) : "left",
                (7,1) : "down",
        }
        
        self.b_policies = {
            (5,2) : self.policy_to_B_5_2,
            (2,0) : self.policy_to_B_2_0,
            (0,0) : self.policy_to_B_0_0,
            (0,3) : self.policy_to_B_0_3,
        }       
    
    def printMsg(self, msg):
        print("**********", msg, "**********")
    
    def sendRead(self, motor_command, sleep, angle=-1, delay = 0.1):
        
        full_command = motor_command + [angle] + [sleep]
        start_time = time.time()
        reading = self.sendRxCommand(full_command, delay) 
        stop_time = time.time()
        
        # print(angle)
        
        self.last_angle = angle
        self.last_motor_commands = motor_command
        self.last_sleep = sleep     
        
        if reading:
            self.readings.append(self.cleanReadings(reading))
            
            # if len(self.readings) > 2:
            #     last_to_last_reading = self.readings[-2].values()
            #     last_reading = self.readings[-1].values()
            #     for r1, r2 in zip(last_reading, last_to_last_reading):
            #         if self.debug:
            #             print(">> Replacing reading")
            #         if r1/r2 >= 2 or r2/r1 >= 2:
            #             self.readings[-1] = last_to_last_reading
            #             break
             
            self.last_reading = Readings(**self.readings[-1])
            
            if self.debug:
                print(">> Time taken", stop_time-start_time)  
                print(">>", self.readings[-1])  
            
            return self.last_reading
        else:
            return None      
    
    def brake(self):
        return self.sendRead([0, 0, 0], 0)
    
    def findClosestSquare(self):
        
        reading = self.brake()
        if reading.front > self.open_threshold:
            reading = self.moveSquare("up")
        elif reading.right > self.open_threshold:
            reading = self.moveSquare("right")
        elif reading.left > self.open_threshold:
            reading = self.moveSquare("left")
        elif reading.back > self.open_threshold:
            reading = self.moveSquare("down")
        
        return reading      
    
    def moveSquare(self, block, feet_to_move = 1):
        
        self.center()
        
        reading = self.brake()
        command, sleep = None, None
        
        if block=="up" and reading.front > self.open_threshold:
            command, sleep = self.forwardCommand(9 * feet_to_move)
        elif block=="down" and reading.back > self.open_threshold:
            command, sleep = self.reverseCommand(12*feet_to_move)
        elif block == "left" and reading.left > self.open_threshold:
            command, sleep = self.slideLeftCommand(10*feet_to_move)
        elif block == "right" and reading.right > self.open_threshold:
            command, sleep = self.slideRightCommand(9.5*feet_to_move)
        # else:
        #     reading = self.findClosestSquare()
        
        if command:
            reading = self.sendRead(command, sleep)
        
        return reading       
    
    def center(self):
        
        # readings = self.brake()
        readings = self.align()

        command = None
        
        if readings.left < readings.right and (readings.left < self.side_threshold):
            # print(readings.left, self.side_threshold)
            command, sleep = self.slideRightCommand(0.3)
        
        elif readings.right < readings.left and (readings.right < self.side_threshold):
            command, sleep = self.slideLeftCommand(0.3)
            
        elif readings.front < self.front_threshold and readings.back > self.front_threshold:
            command, sleep = self.reverseCommand(0.5)
        
        elif readings.back < self.front_threshold and readings.front > self.front_threshold:
            command, sleep = self.forwardCommand(0.5)
        
        if command:
            self.printMsg("Centering")
            readings = self.sendRead(command, sleep)
        
        return readings
    
    def faceNorth(self):
        
        command = None
        self.center()
        
        if self.facing != (0,1):
            
            if self.facing == (0,-1):
                command, sleep = self.turn180(1.3)
            elif self.facing == (-1,0):
                command, sleep = self.turnRightCommand(1.3)
            elif self.facing == (1,0):
                command, sleep = self.turnLeftCommand(1.3)
            else:
                self.sensorLocalize()
                self.faceNorth()
                
        if command:
            self.printMsg("Facing North")
            self.sendRead(command, sleep)   
        
        # self.sensorLocalize()
    
    def followPolicy(self, policy, stopping_criterion):
        
        # self.printMsg("Localize?")
        if not self.location:
            self.sensorLocalize()
        
        # self.printMsg("Face North?")
        self.faceNorth()
        
        self.printMsg("Start policy")
        while not stopping_criterion():
            next_move = policy[self.location]
            self.printMsg("next " + str(next_move))
            
            self.moveSquare(next_move, feet_to_move=0.5)
            self.moveSquare(next_move, feet_to_move=0.5)
            self.changeLocation(next_move)
            
    def changeLocation(self, move):
        
        if move == "up":
            self.location = (self.location[0], self.location[1]+1)
        elif move == "down":
            self.location = (self.location[0], self.location[1]-1)
        elif move == "right":
            self.location = (self.location[0]+1, self.location[1])
        elif move == "left":
            self.location = (self.location[0]-1, self.location[1])       
            
    def checkIfAligned(self):
        
        aligned = False
        readings = self.brake().__dict__
        good_count = 0        
        for sensor in readings:
            if "_" not in sensor:
                if readings[sensor] <= 3:
                    good_count += 1
        if good_count >= 2:
            aligned = True   
        
        return aligned       
    
    def align(self):
        
        readings = self.brake()
        
        if readings.right - self.ir_right > self.align_threshold or readings.left - self.ir_left < self.align_threshold:
            command, sleep = self.turnRightCommand(0.3)
        elif readings.right - self.ir_right < self.align_threshold or readings.left - self.ir_left > self.align_threshold:
            command, sleep = self.turnLeftCommand(0.3)
        
        if command:
            self.printMsg("Aligning")
            return self.sendRead(command, sleep)
        else:
            return readings
    
    def _align(self, timeout = 10):
        
        self.printMsg("Aligning")
        
        aligned = self.checkIfAligned()
        time_elapsed = 0.0
        
        while not aligned or time_elapsed < timeout:
            
            start_time = time.time()
            command = [0,0,0]
            sleep = 0.0
            readings = self.last_reading
            
            if readings.left < readings.right and (readings.left < self.side_threshold or readings.front_left < self.diagonal_threshhold):
                command, sleep = self.slideRightCommand()
            elif readings.right < readings.left and (readings.right < self.side_threshold or readings.front_right < self.diagonal_threshhold):
                command, sleep = self.slideLeftCommand()
            elif readings.front < self.front_threshold * 0.35:
                command, sleep = self.reverseCommand()      
            elif not aligned:
                command, sleep = self.turnRightCommand(0.2)
            
            readings = self.sendRead(command, sleep, 0.0)
            stop_time = time.time()
            time_elapsed += stop_time - start_time
            aligned = self.checkIfAligned()
        
        self.printMsg("Aligned: " + str(aligned))

    def sensorLocalize(self):
        
        self.printMsg("Localizing")
        
        # @ L1
        reading_1 = self.brake()
        
        # @ L2
        reading_2 = self.findClosestSquare()
        
        # print(reading_1.__dict__, "\n", reading_2.__dict__)
        
        predict_facing, predict_l1, predict_l2 = findSqDirectionMultiReadings(reading_1.__dict__, reading_2.__dict__)
        print("Facing {0} from {1} to {2}.".format(predict_facing, predict_l1, predict_l2))

        self.init_localization_done = True
        self.location = predict_l2  
        self.facing = predict_facing     
        
        self.printMsg("Localized")
        # print(reading_1.__dict__, reading_2.__dict__)
    
    def sendRxCommand(self, motor_command, offset_s = 0.1):
    
        ser = self.ser
        
        # Sending
        str_command = commandToStrBytes(motor_command)
        # print('Sending', str_command)
        ser.write(str_command)
        
        sleep(motor_command[-1]/1000 + offset_s) 
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

    def scoop(self, angle):
        self.printMsg("Scoop {} muthafucka".format(angle))
        self.last_angle = angle
        return self.sendRead([0,0,0], sleep=0, angle=angle)
    
    def goToLZ(self):
        
        self.followPolicy(
            self.policy_loading_zone,
            lambda x: True if self.location in [(5,0), (7,2)] else False
        )
    
    def pickUpBlock(self):
        
        # # 1 - Rotate
        # self.printMsg("Turn muthafucka")
        # if self.location == (5,0):
        #     command, sleep = self.turnRightCommand(1.1)
        # elif self.location == (7,2):
        #     command, sleep = self.turn180(1.3)
        
        # self.sendRead(command, sleep)
        
        # 2 - Open up shit
        self.scoop(self.open_angle)
        block = self.blockInFront(block_threshold = self.block_threshold)
        fwd_done, left1_done, left2_done, right1_done, right2_done = [False] * 5
        
        # 3 - Find
        self.printMsg("Finding nemo")
        while not block:
            
            self.center()
            can_go_forward = self.last_reading.front > 8
            can_turn_left = self.last_reading.left > 5 
            can_turn_right = self.last_reading.right > 5
            
            if not can_turn_left and not can_go_forward:
                self.scoop(self.close_angle)
                
                command, sleep = self.forwardCommand(1.2)
                self.sendRead(command, sleep)
                
                command, sleep = self.turnRightCommand(1.3)
                self.sendRead(command, sleep)

                block = self.blockInFront(block_threshold = self.block_threshold)  
                
                if not block:
                    # Turn around
                    command, sleep = self.forwardCommand(0.5)
                    self.sendRead(command, sleep)                
                    
                    command, sleep = self.turnRightCommand(1.3)
                    self.sendRead(command, sleep)
                
                command, sleep = [0,0,0], 0.0
                
            elif not can_turn_right and not can_go_forward:
                self.scoop(self.close_angle)
                
                command, sleep = self.forwardCommand(1.2)
                self.sendRead(command, sleep)
                
                command, sleep = self.turnLeftCommand(1.3)
                self.sendRead(command, sleep)
                
                block = self.blockInFront(block_threshold = self.block_threshold)  
                
                if not block:
                    # Turn around
                    command, sleep = self.forwardCommand(0.5)
                    self.sendRead(command, sleep)                
                    
                    command, sleep = self.turnLeftCCommand(1.3)
                    self.sendRead(command, sleep)
                    
                command, sleep = [0,0,0], 0.0
                
            elif can_go_forward:
                command, sleep = self.forwardCommand(0.5)
                            
            # check ahead of u
            self.sendRead(command, sleep, angle = self.open_angle)
            block = self.blockInFront(block_threshold = self.block_threshold)                  
        
        # 4- Block found, pikckup    
        self.printMsg("Get ready you piece of shit")
        self.scoopItUp(tries = 2)
        
    def scoopItUp(self, tries = 1):
        
        for i in range(tries):
            
            self.scoop(self.open_angle)
            
            # Scoop and go forward
            command, sleep = self.forwardCommand(1.0)
            self.sendRead(command, sleep, angle = self.open_angle)
            
            self.scoop(self.close_angle)
            # self.sendRead(command, sleep, angle = self.close_angle)
            
            # Backup
            command, sleep = self.reverseCommand(0.5)
            self.sendRead(command, sleep)
                
    def blockInFront(self, block_threshold):
        self.scoop(self.open_angle)
        print(self.last_reading.front, self.block_reading )
        if self.last_reading.front - self.block_reading >= 3 and self.block_reading <= block_threshold:
            return True
        return False               
    
    ######## Commands ########
    
    def slideRightCommand(self, multiplier = 1):
        
        self.motor_a_coeff = 1.0
        self.motor_b_coeff = 0.72
        self.motor_c_coeff = 0.9
        
        print('> Slide right')
        command = slideRight(self.motor_a_coeff, self.motor_b_coeff, self.motor_c_coeff, speed = self.slide_speed)
        sleep_req_ms = self.slide_time_ms * multiplier
        
        return command, sleep_req_ms
    
    def slideLeftCommand(self, multiplier = 1):
        
        self.motor_a_coeff = 1.0
        self.motor_b_coeff = 0.72
        self.motor_c_coeff = 0.9
        
        print('> slide left')
        command = slideLeft(self.motor_a_coeff, self.motor_b_coeff, self.motor_c_coeff, speed = self.slide_speed)
        sleep_req_ms = self.slide_time_ms * multiplier
        
        return command, sleep_req_ms
    
    def reverseCommand(self, multiplier = 1):
        
        self.motor_a_coeff = 0.955
        self.motor_b_coeff = 1.0
        self.motor_c_coeff = 0.725        
        
        print('> Reverse')
        command = moveBwd(self.motor_a_coeff, self.motor_b_coeff, self.speed)
        sleep_req_ms = self.reverse_time_ms * multiplier
        
        return command, sleep_req_ms      
    
    def turnRightCommand(self, multiplier = 1):
        
        self.motor_a_coeff = 0.955
        self.motor_b_coeff = 1.0
        self.motor_c_coeff = 0.725  
        
        print('> Turn right')
        command = turnRight(self.motor_a_coeff, self.motor_b_coeff, self.motor_c_coeff, speed=self.turn_speed)
        sleep_req_ms = self.ninty_deg_turn_time_ms * multiplier
        
        return command, sleep_req_ms   
     
    def turnLeftCommand(self, multiplier = 1):
        
        self.motor_a_coeff = 0.955
        self.motor_b_coeff = 1.0
        self.motor_c_coeff = 0.725  
        
        print('> turn left')
        command = turnLeft(self.motor_a_coeff, self.motor_b_coeff, self.motor_c_coeff, speed=self.turn_speed)
        sleep_req_ms = self.ninty_deg_turn_time_ms*multiplier
        
        return command, sleep_req_ms   
     
    def forwardCommand(self, multiplier = 1):
        
        self.motor_a_coeff = 0.955
        self.motor_b_coeff = 1.0
        self.motor_c_coeff = 0.725        
        
        print('> Forward')
        command = moveFwd(self.motor_a_coeff, self.motor_b_coeff, speed = self.speed)
        sleep_req_ms = self.forward_time_ms * multiplier
        
        return command, sleep_req_ms           
     
    def turn180(self, multiplier = 1):
        
        print('> Turn 180')
        command = turnRight(self.motor_a_coeff, self.motor_b_coeff, self.motor_c_coeff, speed=self.turn_speed)
        sleep_req_ms = self.ninty_deg_turn_time_ms * 2 * multiplier
        
        return command, sleep_req_ms
     
    def cleanReadings(self, readings):
        
        # Find mode
        readings = [readings[i*3:i*3+3] for i in range(9)]
        
        cleaned = []
        for reading in readings:
            reading = [int(i) for i in reading]
            cleaned.append(max(reading))
            # cleaned.append(sum(reading) / len(reading))
            # cleaned.append(int(stats.mode(reading)[0]))
        
        # To inches
        cleaned = [i*0.393 for i in cleaned]
        
        # Add offsets in inches
        # f-l, f, f-r, l, r, b, block, ir, ir
        offsets = [1.5,1.5,1.5,0.5,1.5, 0, 0, 0, 0] # when using max(reading)
        cleaned = [cleaned[i] + offsets[i] for i in range(len(offsets))]
        
        # Round
        cleaned = [round(i, 1) for i in cleaned]
        
        reading_map = {
                'front' : cleaned[1],
                'left' : cleaned[3],
                'right' : cleaned[4],
                "front_left" : cleaned[0],
                "front_right" : cleaned[2],
                'back' : cleaned[5],
            }     
        
        # print("fr", reading_map["front-right"])
        # print("fl", reading_map["front-left"])
        if  reading_map["front_right"] > 6:
            reading_map["front_right"] = 4
        if  reading_map["front_left"] > 6:
            reading_map["front_left"] = 4
        
        # Save block reading
        self.block_reading = cleaned[6]
        self.ir_left = cleaned[7]
        self.ir_right = cleaned[8]
        
        return reading_map
    