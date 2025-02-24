import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation

from utils import *
from grid import *
barriers = []

def pointInPolygon(point, polygon):
    # implement ray casting algorithm
    x, y = point.x, point.y
    intersections = 0
    for i in range(len(polygon)):
        x1 = polygon[i][0]
        y1 = polygon[i][1]
        x2 = polygon[(i+1)%len(polygon)][0]
        y2 = polygon[(i+1)%len(polygon)][1]
        
        if y1 != y2:  # Ensure we are not dividing by zero
            if min(y1, y2) < y <= max(y1, y2):  # Strict inequality to avoid touching edges
                x0 = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if x <= x0:  # Strict inequality to avoid touching edges
                    intersections += 1
    
    return intersections % 2 == 1

def checkRange(point):
    if point.x < 0 or point.x >= 50 or point.y < 0 or point.y >= 50:
        print("out of range")
        return False
    return True

def checkPointInPolygon(point):
    for barrier in barriers:
        if pointInPolygon(point, barrier):
            return True
    return False
def gen_polygons(worldfilepath):
    polygons = []
    with open(worldfilepath, "r") as f:
        lines = f.readlines()
        lines = [line[:-1] for line in lines]
        for line in lines:
            polygon = []
            pts = line.split(';')
            for pt in pts:
                xy = pt.split(',')
                polygon.append(Point(int(xy[0]), int(xy[1])))
            polygons.append(polygon)
    return polygons


resPath = []

# unction DEPTH-FIRST-SEARCH(problem) returns a solution node or failure
# frontier <- a LIFO queue (stack) with NODE(problem.INITIAL) as an element
# while not IS-EMPTY(frontier) do
# node <- POP(frontier)
# if problem.IS-GOAL(node.STATE) then return node
# for each child in EXPAND(problem, node) do
# if not IS-CYCLE(child) do
# add child to frontier
# return result
def dfs(source, dest):
    res_path = []
    frontier = Stack()  # Correct instantiation
    frontier.push(source)  # Initialize stack with the source point and path
    visited = set()
    visited.add((source.x, source.y))

    while not frontier.isEmpty():
        current = frontier.pop()
        res_path.append(current)
        if current.x == dest.x and current.y == dest.y:
            return res_path
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = Point(current.x + dx, current.y + dy)
            if (neighbor.x, neighbor.y) not in visited and checkRange(neighbor) and not checkPointInPolygon(neighbor):
                frontier.push((neighbor))
                visited.add((neighbor.x, neighbor.y))

    return res_path

if __name__ == "__main__":
    epolygons = gen_polygons('TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('TestingGrid/world1_turfs.txt')

    source = Point(8,10)
    dest = Point(43,45)

    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point
    
    # Draw enclosure polygons
     # Draw enclosure polygons
    
    for polygon in epolygons:
        barrier = []
        for p in polygon:
            draw_point(ax, p.x, p.y)
            barrier.append((p.x, p.y))
        barriers.append(barrier)
    print(barriers)
    
            
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])
    
    # Draw turf polygons
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

    res_path = dfs(source, dest)
    
    for i in range(len(res_path)-1, 0, -1):
        draw_result_line(ax, [res_path[i].x, res_path[i-1].x], [res_path[i].y, res_path[i-1].y])
        plt.pause(0.1)
   
    plt.show()

