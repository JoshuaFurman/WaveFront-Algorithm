import numpy as np
import math
import Queue as queue

# This function is used while reading in the configuration space
def format_array(array):
    new_array = []
    for x in array.split():
        new_array.append(int(x))
    return new_array

# This function returns an array of neighboring points while checking for out of
# bounds errors
def get_neighbors(world,i,j,k):
    neighbors = []
    if (i-1) >= 0:
        neighbors.append([i-1,j,k])

    if (i-1) >= 0 and (j-1) >= 0:
        neighbors.append([i-1,j-1,k])

    if (i-1) >= 0 and (j+1) != y_upper:
        neighbors.append([i-1,j+1,k])

    if (i-1) >= 0 and (k-1) >= 0:
        neighbors.append([i-1,j,k-1])

    if (i-1) >= 0 and (k+1) != z_upper:
        neighbors.append([i-1,j,k+1])

    if (j-1) >= 0:
        neighbors.append([i,j-1,k])

    if (j-1) >= 0 and (k-1) >= 0:
        neighbors.append([i,j-1,k-1])

    if (j-1) >= 0 and (k+1) != z_upper:
        neighbors.append([i,j-1,k+1])

    if (k-1) >= 0:
        neighbors.append([i,j,k-1])

    if (i-1) >= 0 and (j-1) >= 0 and (k-1) >= 0:
        neighbors.append([i-1,j-1,k-1])

    if (i+1) != x_upper and (j-1) >= 0 and (k-1) >= 0:
        neighbors.append([i+1,j-1,k-1])

    if (i-1) >= 0 and (j+1) != y_upper and (k-1) >= 0:
        neighbors.append([i-1,j+1,k-1])

    if (i-1) >= 0 and (j-1) >= 0 and (k+1) != z_upper:
        neighbors.append([i-1,j-1,k+1])

    if (i+1) != x_upper and (j+1) != y_upper and (k-1) >= 0:
        neighbors.append([i+1,j+1,k-1])

    if (i+1) != x_upper and (j-1) >= 0 and (k+1) != z_upper:
        neighbors.append([i+1,j-1,k+1])

    if (i-1) >= 0 and (j+1) != y_upper and (k+1) != z_upper:
        neighbors.append([i-1,j+1,k+1])

    if (i+1) != x_upper:
        neighbors.append([i+1,j,k])

    if (i+1) != x_upper and (j+1) != y_upper:
        neighbors.append([i+1,j+1,k])

    if (i+1) != x_upper and (k+1) != z_upper:
        neighbors.append([i+1,j,k+1])

    if (j+1) != y_upper and (k+1) != z_upper:
        neighbors.append([i,j+1,k+1])

    if (j+1) != y_upper:
        neighbors.append([i,j+1,k])

    if (k+1) != z_upper:
        neighbors.append([i,j,k+1])

    if (i+1) != x_upper and (j+1) != y_upper and (k+1) != z_upper:
        neighbors.append([i+1,j+1,k+1])

    return neighbors

# This function calls the get neighbors function and returns the neighbor of the
# node with the nodes value minus 1
def get_smallest_neighbor(world,i,j,k):
    children = get_neighbors(world,i,j,k)
    for child in children:
        if world[child[0],child[1],child[2]] == -1:
            children.remove([child[0],child[1],child[2]])

    smallest = world[children[0][0],children[0][1],children[0][2]]
    next_point = [children[0][0],children[0][1],children[0][2]]
    for kid in children:
        if world[kid[0],kid[1],kid[2]] < smallest and world[kid[0],kid[1],kid[2]] != -1:
            next_point = [kid[0],kid[1],kid[2]]

    return next_point

# This function is used while creating the spheres in the configuration space
def sphere_distance(x, y, z, x_center, y_center, z_center):
    x1 = math.pow((x - x_center), 2)
    y1 = math.pow((y - y_center), 2)
    z1 = math.pow((z - z_center), 2)
    return (x1 + y1 + z1)

# This function adds a cube to the world space
def add_cube(world, x, y, z, x_center, y_center, z_center, length):
    j = 0
    k = 0
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if i >= abs(x_center - math.ceil((length/2))) and i <= abs(x_center + math.ceil((length/2))):
                    if j >= abs(y_center - math.ceil((length/2))) and j <= abs(y_center + math.ceil((length/2))):
                        if k >= abs(z_center - math.ceil((length/2))) and k <= abs(z_center + math.ceil((length/2))):
                            world[i,j,k] = -1

# This function adds a sphere to the configuration space
def add_sphere(world, x, y, z, x_center, y_center, z_center, radius):
    j = 0
    k = 0
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if sphere_distance(i,j,k,x_center,y_center,z_center) <= math.pow(radius, 2):
                    world[i,j,k] = -1

# This function reads in data from a file and creates the world space with
# obstacles
def create_world_space(file):

    global start
    global goal
    global x_upper
    global y_upper
    global z_upper

    with open(file, 'r') as f:
        data = f.readlines()

        x_axis = format_array(data[0])
        y_axis = format_array(data[1])
        z_axis = format_array(data[2])
        cube1 = format_array(data[3])
        cube2 = format_array(data[4])
        sphere1 = format_array(data[5])
        sphere2 = format_array(data[6])
        start = format_array(data[7])
        goal = format_array(data[8])

    x_upper = x_axis[1] - x_axis[0] + 1
    y_upper = y_axis[1] - y_axis[0] + 1
    z_upper = z_axis[1] - z_axis[0] + 1

    world = np.zeros([x_upper,y_upper,z_upper],dtype=np.int)

    add_cube(world,x_upper,y_upper,z_upper,cube1[0],cube1[1],cube1[2],cube1[3]+1)
    add_cube(world,x_upper,y_upper,z_upper,cube2[0],cube2[1],cube2[2],cube2[3]+1)

    add_sphere(world,x_upper,y_upper,z_upper,sphere1[0],sphere1[1],sphere1[2],sphere1[3]+1)
    add_sphere(world,x_upper,y_upper,z_upper,sphere2[0],sphere2[1],sphere2[2],sphere2[3]+1)

    world[goal[0],goal[1],goal[2]] = 2

    return world

# This function implements the wavefront algorithm by a BFS for populating the
# values in the 3D array and outputs an array moving from the start to the goal
def wavefront(world, start_, end):
    fringe = queue.Queue()

    fringe.put(end)

    while fringe.empty() != True:
        point = fringe.get()

        if point == start_:
            break

        children = get_neighbors(world, point[0],point[1],point[2])
        for child in children:
            if world[child[0],child[1],child[2]] != 0:
                continue
            elif world[child[0],child[1],child[2]] == -1:
                continue
            else:
                world[child[0],child[1],child[2]] = world[point[0],point[1],point[2]] + 1
                fringe.put(child)

    i = start_[0]
    j = start_[1]
    k = start_[2]
    path = []

    while (world[i,j,k] != 2):
        path.append([i,j,k])

        next_point = get_smallest_neighbor(world,i,j,k)

        i = next_point[0]
        j = next_point[1]
        k = next_point[2]

    path.append([i,j,k])

    return path

# This prompts the user to input the name of the file to be read in
file_name = raw_input("Please enter the file name you would like to create the world from: ")
world_space = create_world_space(file_name)

# This calls the wavefront algorithm and stores the path in the variable path
print("\nGenerating WaveFront and getting path....")
path = wavefront(world_space, start, goal)

# This writes the data stored in the path array to an output file
with open('WaveFront_output.txt', 'w') as f:
    for point in path:
        f.write('%d,%d,%d\n' % (point[0],point[1],point[2]))
print("\nA path has been written to the file: WaveFront_output.txt")
