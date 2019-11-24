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
    # hyp = maze_step_size * (x_dir**2 + y_dir**2) ** 0.5
    hyp = maze_step_size
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
        
        try:
            if maze[col, row] == 1:
                wall_found = True
        except:
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
        # print(sensor_pos)
        # print(sensor, sensor_pos)
        dist_to_wall = findDist(maze, sensor_pos, sensor_direction)        
        distances[sensor] = dist_to_wall
    
    return distances

################# Comparison functions #################

def findMatchNorm(sensor_distances, sensor_data, debug = False):
    
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

def findAvgDelta(r1, r2):
    diff_vector = []
    for sensor in r1:
        diff_vector.append(abs(r1[sensor] - r2[sensor]))  
            
    diff = sum(diff_vector) / len(diff_vector)
    
    return diff

def findMaxDelta(r1, r2):
    diff_vector = []
    for sensor in r1:
        diff_vector.append(abs(r1[sensor] - r2[sensor]))  
            
    diff = max(diff_vector) 
    
    return diff

def findMatch(sensor_distances, sensor_data, debug = False):
    
    min_diff_found = 1e6
    min_pos = None
    for row in range(sensor_distances.shape[0]):
        for col in range(sensor_distances.shape[1]):
            test_data = sensor_distances[row, col]
            if test_data:
                diff = findAvgDelta(sensor_data, test_data)   
                if diff < min_diff_found:
                    min_diff_found = diff
                    min_pos = (row, col)
    if debug:
        return min_pos, min_diff_found
    else:
        return min_pos

def findMatches(sensor_distances, sensor_data):
    
    diffs = []
    positions = []
    for row in range(sensor_distances.shape[0]):
        for col in range(sensor_distances.shape[1]):
            test_data = sensor_distances[row, col]
            if test_data:
                diffs.append(findAvgDelta(sensor_data, test_data))
                positions.append((row, col))
    
    diffs, positions = zip(*sorted(zip(diffs, positions)))        
    
    return positions[:3]

def addNoise(sensor_data, inches = 2):
    
    sensor_data = {a:b+inches for a,b in sensor_data.items()}

    return sensor_data

def addRandomNoise(sensor_data, inches = 2):
    
    sensor_data = {a:b+inches*np.random.random() for a,b in sensor_data.items()}

    return sensor_data

def findDuplicates(sensor_matrix, max_noise = 2, allow_print=False):

    dupicates = []
    for col in range(sensor_matrix.shape[0]):
        for row in range(sensor_matrix.shape[1]):
            if sensor_matrix[col, row]:
                for j in range(10):
                    for i in range(-1, 2, 2):
                        predicted_block = findMatch(sensor_matrix, addNoise(sensor_matrix[col, row], np.random.randint(0,1) * i * max_noise))
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
        
    # if predicted_block in duplicates:
    #     # print("Got duplciate", predicted_block)
    #     return None
    
    return result

def findDirectionLocation(sensor_data):
    
    predicted_positions = []
    predicted_distances = []
    directions = []
    for direc in matrices:
        result = findSquare(direc, sensor_data, debug=True)
        dsit = 1e6
        pos = None
        if result:
            pos, dist = result
        
        predicted_distances.append(dist)
        predicted_positions.append(pos)
        directions.append(direc)
    
    min_dist = min(predicted_distances)
    pos_prediction = predicted_positions[predicted_distances.index(min_dist)]
    direction_prediction = directions[predicted_distances.index(min_dist)]
        
    # if pos_prediction in list([list(block) for block in squares_to_avoid]):
    if pos_prediction in matrices[direction_prediction][1] or pos_prediction in list([list(block) for block in squares_to_avoid]):
        return None, None
    
    return pos_prediction, direction_prediction
  
def findSqDirectionMultiReadings(r1, r2):
    
    directions = {}    
    for direction in matrices:
        directions[direction] = []
        matrix = matrices[direction][0]        
        # predict_l1, l1_diff = findMatch(matrix, r1, debug=True)
        l1_predictions = findMatches(matrix, r1) 
        
        for predict_l1 in l1_predictions:
            # for each direction around it, check:
            positions_checked = []
            diffs = []
            for col,row in [
                (0,1), (0,-1), (-1,0), (1,0)
            ]:
                pos_to_check = (predict_l1[0] + col, predict_l1[1] + row)
                try:
                    if matrix[pos_to_check]:
                        # print("Positon checking", pos_to_check)
                        test_reading = matrix[pos_to_check]
                        diffs.append(findAvgDelta(r2, test_reading))
                        positions_checked.append(pos_to_check)
                except:
                    pass
                                
            l2_diff = min(diffs)
            predict_l2 = positions_checked[diffs.index(l2_diff)]       
            
            # save predictions
            directions[direction].append(predict_l1)
            directions[direction].append(predict_l2)
            directions[direction].append(l2_diff) # record total error
    
    # Find best prediction
    # print(directions)
    min_error = 1e6
    best_dir_found = None
    best_l1 = None
    best_l2 = None
    
    for direction in directions:
        for i in range(0, len(directions[direction]), 3):
            l1_predict = directions[direction][i]
            l2_predict = directions[direction][i+1]
            error = directions[direction][i+2]
            if error < min_error:
                min_error = error
                best_dir_found = direction
                best_l1 = l1_predict
                best_l2 = l2_predict

    # returns direction, l1, l2 
    return best_dir_found, best_l1, best_l2                       
          
################## Make sensor data ##################

maze = createMaze()
matrices = {
    (0,1) : [],
    (0,-1) : [],
    (1,0) : [],
    (-1,0) : []
}

for direction in matrices:
    matrices[direction].append(createSensorMatrix(maze, getSensors(direction), robot_radius=2))
    matrices[direction].append(findDuplicates(matrices[direction][0], 6))

# Find out which squares to avoid
squares_to_avoid = [(3,3), (6,3), (0,3)]
for direction in matrices:
    squares_to_avoid += matrices[direction][1]
squares_to_avoid = np.unique(np.array(squares_to_avoid), axis=0)