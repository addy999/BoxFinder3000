import numpy as np

################# Create matrix #################

def fillInBlocks(matrix, step_size_in, row_min, row_max, col_min, col_max):
    ''' For a block bottom left and top right coordinates in inches'''
    for row in range(int(row_min/step_size_in), np.clip(int(row_max/step_size_in+1), 0, matrix.shape[0])):
        for col in range(int(col_min/step_size_in), np.clip(int(col_max/step_size_in+1), 0, matrix.shape[1])):
            matrix[row+1][col+1] = 1
    
    return matrix

def createMatrix(step_size_in = 3):
    spacing = 12 / step_size_in
    matrix = np.zeros((int(4 * spacing) + 2, int(8 * spacing) + 2))

    rows, cols = matrix.shape
    
    ## top and bottom
    for i in range(cols):
        matrix[0][i] = 1
        matrix[-1][i] = 1    
    ## left and right sides
    for row in range(rows):
        matrix[row][0] = 1
        matrix[row][-1] = 1
        
    matrix = fillInBlocks(matrix, step_size_in, 2*12, 4*12, 12, 24)
    matrix = fillInBlocks(matrix, step_size_in, 0, 12, 12, 24)
    matrix = fillInBlocks(matrix, step_size_in, 0, 12, 36, 48)
    matrix = fillInBlocks(matrix, step_size_in, 24, 36, 36, 60)
    matrix = fillInBlocks(matrix, step_size_in, 12, 24, 60, 12*6)
    matrix = fillInBlocks(matrix, step_size_in, 24, 36, 12*6, 12*7)
    
    return matrix.transpose(), createSensorMatrix(matrix, step_size_in).transpose()

def findDist(matrix, step_size_in, spot, direction):
    x_dir = direction[0]
    y_dir = direction[1]
    hyp = step_size_in * (x_dir**2 + y_dir**2) ** 0.5
    wall_found = False
    traversed = 0
    col, row = int(spot[0])+1, int(spot[1])+1
    
    while not wall_found:
        row += y_dir
        col += x_dir
        traversed += hyp
        
        if matrix[row, col] == 1:
            wall_found = True
            
    return traversed

def createSensorMatrix(matrix, step_size_in):
    sensor_dir = {
        'front' : (0,1),
        'left' : (-1,0),
        'right' : (1,0),
        'back' : (0,-1),
        'front-left' : (-1,1),
        'front-right' : (1,1),
    }

    shape = matrix.shape
    sensor_distances = np.ndarray((shape[0]-2, shape[1]-2), dtype=np.object)
    sensor_distances.shape

    for row in range(sensor_distances.shape[0]):
        for col in range(sensor_distances.shape[1]):
            if matrix[row-1,col-1] == 1:
                pass
            distances = dict(zip(sensor_dir.keys(), np.zeros(6)))
            for direction, dir_tuple in sensor_dir.items():
                dist = findDist(matrix, step_size_in, (col, row), dir_tuple)
                distances[direction] = dist
                
            sensor_distances[row, col] = distances
            
    return sensor_distances

################# Comparison functions #################

def compareDistArrays(dict1, dict2, threshold = 1):
    '''threhsold in inches'''
    arr1 = np.array(list(dict1.values()))
    arr2 = np.array(list(dict2.values()))
    for val1,val2 in zip(arr1,arr2):
        if abs(val1-val2) > threshold:
            return False
    
    return True

def findMatches(sensor_distances, sensor_data, threshold):
    found = []
    for row in range(sensor_distances.shape[0]):
        for col in range(sensor_distances.shape[1]):
            true_dist = sensor_distances[row, col]
            if compareDistArrays(true_dist, sensor_data, threshold):
                found.append((row, col))
    return found

def findMatch(sensor_distances, sensor_data):
    min_dist_found = 1e6
    min_pos = None
    for row in range(sensor_distances.shape[0]):
        for col in range(sensor_distances.shape[1]):
            test_data = sensor_distances[row, col]
            diff_vector = []
            for sensor_dist, test_dist in zip(sensor_data.values(), test_data.values()):
                diff_vector.append(sensor_dist - test_dist)   
            diff = abs(np.linalg.norm(diff_vector))         
            if diff < min_dist_found:
                min_dist_found = diff
                min_pos = (row, col)
                
    return min_dist_found, min_pos
