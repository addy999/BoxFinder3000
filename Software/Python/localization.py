import numpy as np
import copy

################# Create maze #################

maze_step_size = 1

def getSensors(direction = (0,1)):
    
    # dir : [direction, offset]
    
    if direction == (0,1):
        sensors = {
            'front' : [(0,1), (0, 1)],
            'left' : [(-1,0), (-1, 0)],
            'right' : [(1,0), (1, 0)],
            'back' : [(0,-1), (0, -1)],
            'front-left' : [(-1,2), (-1, 1)],
            'front-right' : [(1,2), (1, 1)],
        }
        
    if direction == (0,-1):
        sensors = {
            'front' : [(0,-1), (0, -1)],
            'left' : [(1,0), (1, 0)],
            'right' : [(-1,0), (-1, 0)],
            'back' : [(0,1), (0, 1)],
            'front-left' : [(1,-2), (1, -1)],
            'front-right' : [(-1,-2), (-1, -1)],
        }
    if direction == (-1,0):
        sensors = {
            'front' : [(-1,0), (-1, 0)],
            'left' : [(0,-1), (0, -1)],
            'right' : [(0,1), (0, 1)],
            'back' : [(1,0), (1, 0)],
            'front-left' : [(-2,-1), (-1, -1)],
            'front-right' : [(-2,1), (-1, 1)],
        }
    if direction == (1,0):
        sensors = {
            'front' : [(1,0), (1, 0)],
            'left' : [(0,1), (0, 1)],
            'right' : [(0,-1), (0, -1)],
            'back' : [(-1,0), (-1, 0)],
            'front-left' : [(2,1), (1, 1)],
            'front-right' : [(2,-1), (1, -1)],
        }
    
    return sensors

def fillInBlocks(maze, col_min, col_max, row_min, row_max):
    ''' For a block bottom left and top right coordinates in inches'''
    for row in range(int(col_min/maze_step_size), np.clip(int(col_max/maze_step_size+1), 0, maze.shape[0])):
        for col in range(int(row_min/maze_step_size), np.clip(int(row_max/maze_step_size+1), 0, maze.shape[1])):
            maze[row+1][col+1] = 1
    
    return maze

def createMaze():
    
    spacing = 12 / maze_step_size
    maze = np.zeros((int(8 * spacing) + 2, int(4 * spacing) + 2))

    rows, cols = maze.shape
    
    ## top and bottom
    for i in range(cols):
        maze[0][i] = 1
        maze[-1][i] = 1    
    ## left and right sides
    for row in range(rows):
        maze[row][0] = 1
        maze[row][-1] = 1
        
    maze = fillInBlocks(maze, 12, 24, 2*12, 4*12)
    maze = fillInBlocks(maze, 12, 24, 0, 12)
    maze = fillInBlocks(maze, 36, 48, 0, 12)
    maze = fillInBlocks(maze, 36, 60, 24, 36)
    maze = fillInBlocks(maze, 60, 12*6, 12, 24)
    maze = fillInBlocks(maze, 12*6, 12*7, 24, 36)
    
    # print(maze[:,1])
    
    return maze

def findDist(maze, spot, direction):
    x_dir = direction[0]
    y_dir = direction[1]
    hyp = maze_step_size * (x_dir**2 + y_dir**2) ** 0.5
    wall_found = False
    traversed = 0
    col, row = int(spot[0])+1, int(spot[1])+1
    
    # Check if actally ON a wall
    if maze[col, row] == 1:
        wall_found = True
    
    # If not, find a wall in the direction
    while not wall_found:
        row += y_dir
        col += x_dir
        traversed += hyp
        
        if maze[col, row] == 1:
            wall_found = True
            
    return traversed

def createSensorMatrix(maze, sensors, robot_center = (6,6), robot_radius = (9.4 + 9.95) / 2 / 2):
    
    sensor_distances = np.ndarray((8, 4), dtype=np.object)

    for col in range(sensor_distances.shape[0]):
        for row in range(sensor_distances.shape[1]):
            
            block = (col, row)
            block_distances = createSensorMatrixBlock(maze, sensors, block, robot_center, robot_radius)    
            
            if list(block_distances.values()).count(0) == 6:
                sensor_distances[block] = None
            else:
                sensor_distances[block] = block_distances
            
    return sensor_distances

def createSensorMatrixBlock(maze, sensors, block, robot_center = (6,6), robot_radius = (9.4 + 9.95) / 2 / 2):
    
    # print("Radius", robot_radius)
    robot_center_pos = (12 * block[0] + robot_center[0], 12 * block[1] + robot_center[1])
    distances = copy.deepcopy(sensors)
    
    for sensor in sensors:
        sensor_direction = sensors[sensor][0]
        sensor_offset = sensors[sensor][1]
        
        sensor_pos = [robot_center_pos[i] + int(robot_radius) * sensor_offset[i] for i in range(2)]
        
        # print(sensor, sensor_pos)
        dist_to_wall = findDist(maze, sensor_pos, sensor_direction)        
        distances[sensor] = dist_to_wall
    
    return distances

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

def findMatch(sensor_distances, sensor_data, debug = False):
    
    min_dist_found = 1e6
    min_pos = None
    for row in range(sensor_distances.shape[0]):
        for col in range(sensor_distances.shape[1]):
            test_data = sensor_distances[row, col]
            if test_data:
                diff_vector = []
                for sensor_dist, test_dist in zip(sensor_data.values(), test_data.values()):
                    diff_vector.append(sensor_dist - test_dist)   
                diff = abs(np.linalg.norm(diff_vector))         
                if diff < min_dist_found:
                    min_dist_found = diff
                    min_pos = (row, col)
    if debug:
        return min_pos, min_dist_found
    else:
        return min_pos

def addNoise(sensor_data, inches = 2):
    
    sensor_data = {a:b+inches*np.random.random() for a,b in sensor_data.items()}

    return sensor_data

def findDuplicates(sensor_matrix, max_noise = 2, allow_print=False):

    dupicates = []
    for col in range(sensor_matrix.shape[0]):
        for row in range(sensor_matrix.shape[1]):
            if sensor_matrix[col, row]:
                predicted_block = findMatch(sensor_matrix, addNoise(sensor_matrix[col, row], max_noise))

                if predicted_block != (col,row):
                    dupicates.append(predicted_block)
                    dupicates.append((col,row))
                    if allow_print:
                        print("Testing", [col, row], "Got", predicted_block)
                        print("Expected", sensor_matrix[col, row], "\nGot", sensor_matrix[predicted_block])
                        print("****************")

    if allow_print: 
        print('Mismatched %', 50 * len(dupicates)/sensor_matrix.size)

    return dupicates

def findSquare(direction, sensor_data, debug = False):
    
    result = findMatch(matrices[direction][0], sensor_data, debug)
    duplicates = matrices[direction][1]
    # print(result)
    if debug:
        predicted_block = result[0]
    else:
        predicted_block = result
        
    if predicted_block in duplicates:
        # print("Got duplciate", predicted_block)
        return None
    
    return result
    
################## Make sensor data ##################

maze = createMaze()
matrices = {
    (0,1) : [],
    (0,-1) : [],
    (1,0) : [],
    (-1,0) : []
}

for direction in matrices:
    matrices[direction].append(createSensorMatrix(maze, getSensors(direction)))
    matrices[direction].append(findDuplicates(matrices[direction][0], 6))