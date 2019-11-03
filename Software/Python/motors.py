def moveStraight(motor_a_coeff=1.0, motor_b_coeff=1.0,  speed = 1.0, direction = 1):
    ''' a,b,c '''
    return [
        255 * speed * direction * motor_a_coeff,
        -255 * speed * direction * motor_b_coeff,
        0.0
    ]

def slideLeft(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed = 1.0):
    ''' a,b,c '''
    return [
        125 * speed * motor_a_coeff, 
        125 * speed * motor_b_coeff, 
        -255 * speed * motor_c_coeff
    ]

def slideRight(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed = 1.0):
    ''' a,b,c '''
    return slideLeft(motor_a_coeff, motor_b_coeff, motor_c_coeff, speed) * -1

def turn(motor_a_coeff=1.0, motor_b_coeff=1.0, motor_c_coeff=1.0, speed=1.0, direction=1):
    ''' a,b,c '''
    return [
        255 * speed * direction * motor_a_coeff, 
        255 * speed * direction * motor_b_coeff, 
        255 * speed * direction * motor_c_coeff
    ]