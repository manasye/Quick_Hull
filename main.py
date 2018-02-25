import random
import time
import math
import matplotlib.pyplot as plt

list_of_hull = []

# Function to calculate determinant of three given points
# Equation gathered from Rinaldi's Munir slide -> Penyelesaian Persoalan Convex Hull dengan Divide and Conquer (Quick Hull)
def calculate_determinant(point_1,point_2,point_3):
    return (point_1[0] * point_2[1]) + (point_1[1] * point_3[0]) + (point_2[0] * point_3[1]) - (point_3[0] * point_2[1]) - (point_3[1] * point_1[0]) - (point_2[0] * point_1[1])

# Function to determine the minimum and maximum absis value in list of points
def find_min_and_max(list_of_points):
    minimum_point = list_of_points[0]
    maximum_point = list_of_points[0]

    for point in list_of_points:
        if(point[0] <= minimum_point[0]):
            minimum_point = point
        if(point[0] >= maximum_point[0]):
            maximum_point = point

    return minimum_point,maximum_point

# Function to calculate point distance toward a line made by two points
def calc_line_dist(min_absis,max_absis,point):
    return abs((point[1] - min_absis[1]) * (max_absis[0] - min_absis[0]) - (max_absis[1] - min_absis[1]) * (point[0] - min_absis[0]))

# Function that divide left side points
def divide_side(points,min_absis,max_absis):
    left_hull = []
    right_hull = []

    for point in points:
        if(point != min_absis) and (point != max_absis):
            # Skip the dummy point
            if (calculate_determinant(min_absis,max_absis,point) > 0):
                left_hull.append(point)
            # Skip the dummy point
            if (calculate_determinant(min_absis,max_absis,point) < 0):
                right_hull.append(point)

    return left_hull,right_hull

# Function to find max distance
def find_max_distance(points,min_absis,max_absis):
    max_distance = 0
    index_of_max = 0

    for i in range(0,len(points)):
        curr_distance = calc_line_dist(min_absis,max_absis,points[i])
        if curr_distance > max_distance:
            index_of_max = i
            max_distance = curr_distance

    return points[index_of_max]

# Function that do the left quick hull
def quick_hull_left(points,min_absis,max_absis):
    # Recurens stop where no point found
    if(len(points) == 0):
        return
    # Recurens continue
    else:
        max_point = find_max_distance(points,min_absis,max_absis)
        points.remove(max_point)
        list_of_hull.append(max_point)
        first_side,_ = divide_side(points,min_absis,max_point)
        second_side,_ = divide_side(points,max_point,max_absis)
        # Get the left part only (right part is dummy)
        quick_hull_left(first_side,min_absis,max_point)
        quick_hull_left(second_side,max_point,max_absis)

# Function that do the right quick hull
def quick_hull_right(points,min_absis,max_absis):
    # Recurens stop where no point found
    if(len(points) == 0):
        return
    # Recurens continue
    else:
        max_point = find_max_distance(points,min_absis,max_absis)
        points.remove(max_point)
        list_of_hull.append(max_point)
        _,first_side = divide_side(points,min_absis,max_point)
        _,second_side = divide_side(points,max_point,max_absis)
        # Getting the right part only(left part is dummy)
        quick_hull_right(first_side,min_absis,max_point)
        quick_hull_right(second_side,max_point,max_absis)

# Function that do the first quick hull
def quick_hull_parent(points,min_absis,max_absis):
    left_hull,right_hull = divide_side(points,min_absis,max_absis)
    list_of_hull.append(min_absis)
    list_of_hull.append(max_absis)
    quick_hull_left(left_hull,min_absis,max_absis)
    quick_hull_right(right_hull,min_absis,max_absis)

if __name__ == '__main__':
    num_of_points = int(input('Input numbers of point : '))
    points = []
    # Generate random coordinate
    for i in range(0,num_of_points):
        points.append([])
        points[i].append(random.randint(-100,100))
        points[i].append(random.randint(-100,100))
        plt.plot(points[i][0],points[i][1],"o")

    print('Points generated is: '+ str(points))
    min_absis,max_absis = find_min_and_max(points)
    tuple_of_hull = []
    time_begin = time.clock()

    quick_hull_parent(points,min_absis,max_absis)

    time_end = time.clock()
    central_x = sum(point[0] for point in list_of_hull)/len(list_of_hull)
    central_y = sum(point[1] for point in list_of_hull)/len(list_of_hull)
    list_of_hull.sort(key = lambda point: math.atan2(point[0] - central_x, point[1] - central_y))

    # Make the tuple of list of hull
    for i in range(0,len(list_of_hull)):
        if(i == len(list_of_hull)-1):
            tuple_of_hull.append([list_of_hull[i],list_of_hull[0]])
        else:
            tuple_of_hull.append([list_of_hull[i],list_of_hull[i+1]])

    print('Quick Hull result is: '+ str(tuple_of_hull))
    print('Quick Hull took: ' + str(time_end - time_begin) + ' s')

    for x in range(0,len(tuple_of_hull)):
        list_of_x = [tuple_of_hull[x][0][0],tuple_of_hull[x][1][0]]
        list_of_y = [tuple_of_hull[x][0][1],tuple_of_hull[x][1][1]]
        plt.plot(list_of_x,list_of_y,color="#6A1B9A")

    plt.title('Quick Hull - 13516122')
    plt.show()
