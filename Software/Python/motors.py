def moveFwd(motor_a_coeff=1.0, motor_b_coeff=1.0, speed = 1.0):
    ''' straight by default'''
    return [
        -255 * speed * motor_a_coeff,
        255 * speed * motor_b_coeff,
        0.0
    ]
    
def moveBwd(motor_a_coeff=1.0, motor_b_coeff=1.0, speed = 1.0):
    ''' straight by default'''
    return [i*-1 for i in moveFwd(motor_a_coeff, motor_b_coeff, speed)]

def slideLeft(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed = 1.0):
    ''' a,b,c '''
    return [
        125 * speed * motor_a_coeff, 
        125 * speed * motor_b_coeff, 
        -255 * speed * motor_c_coeff
    ]

def slideRight(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed = 1.0):
    ''' a,b,c '''
    return [i * -1 for i in slideLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed)]

def turnLeft(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed=1.0):
    return [
        255 * speed * motor_a_coeff, 
        255 * speed * motor_b_coeff, 
        255 * speed * motor_c_coeff
    ]
    
def turnRight(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed=1.0):
    return [i*-1 for i in turnLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed)]