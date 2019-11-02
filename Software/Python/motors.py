def moveStraight(speed = 1.0, direction = 1):
    ''' a,b,c '''
    return [255 * speed * direction, -255 * speed * direction, 0.0]

def moveLeft(speed = 1.0, direction = 1):
    ''' a,b,c '''
    return [255 * speed * direction / 2, -255 * speed * direction / 2 , 255 * speed * direction]

def moveRight(speed = 1.0):
    ''' a,b,c '''
    return moveLeft(speed) * -1

def turn(speed, direction):
    ''' a,b,c '''
    return []