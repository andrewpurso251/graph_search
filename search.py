import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation

from utils import *
from grid import *
barriers = []

def pointInPolygon(point, polygon):
    x = point.x
    y = point.y

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
def dfs():
    res_path = []
    
    
    sourceX = 8
    sourceY = 10
    destX = 43
    destY = 45

    queue = Queue()
    queue.push(source)
    visited = set()
    visited.add((source.x, source.y))

    while not queue.isEmpty():
        current = queue.pop()
        res_path.append(current)
        if current.x == destX and current.y == destY:
            return res_path
        
        # get coordinates
        if current.y + 1 < 50:
            up = Point(current.x, current.y + 1)
            if (up.x, up.y) not in visited:
                queue.push(up)
                visited.add((up.x, up.y))
        if current.x + 1 < 50:    
            right = Point(current.x + 1, current.y)
            if (right.x, right.y) not in visited:
                queue.push(right)
                visited.add((right.x, right.y))
            
        if current.y - 1 >= 0:
            down = Point(current.x, current.y - 1)
            if (down.x, down.y) not in visited:
                queue.push(down)
                visited.add((down.x, down.y))
            
        if current.x - 1 >= 0:
            left = Point(current.x - 1, current.y)
            if (left.x, left.y) not in visited:
                queue.push(left)
                visited.add((left.x, left.y))

        
                

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

    res_path = dfs()
    
    for i in range(len(res_path)-1):
        draw_result_line(ax, [res_path[i].x, res_path[i+1].x], [res_path[i].y, res_path[i+1].y])
        plt.pause(0.1)
   
    plt.show()
    
