import random
import pygame

conv = [(1, 0), (0, -1), (-1, 0), (0, 1)]
def initialize(state, n):
    for i in range(n):
        state.append([])
        for j in range(n):
            state[i].append([0, 0, 0, 0, 0])

def percolate(state, n, p):
    for i in range(n):
        for j in range(n):
            for k in range(1, 3):
                if random.random() < p:
                    delete(state, i, j, k)

def bfs_subiterative(state, n, x, y, mark):
    count = 0
    
    queue = []

    state[x][y][4] = mark
    queue.append((x,y))

    while queue != []:
        v = queue.pop(0)
        
        i, j = v
        for neighbour in neighbours(state, n, i, j):
            i2, j2 = neighbour
            
            if state[i2][j2][4] == 0:
                state[i2][j2][4] = mark
                count += 1
                
                queue.append(neighbour)

    return count

def bfs_iterative(state, n):
    mark = 1

    maxcount = -1
    
    for i in range(1, n):
        for j in range(1, n):
            if state[i][j][4] == 0:
                mark += 1
                
                count = bfs_subiterative(state, n, i, j, mark)
                if count > maxcount:
                    maxcount = count
                    maxid = mark
    return maxid

def neighbours(state, n, x, y):
    neighbours_list = []
    
    for direction in range(4):
        x2, y2 = conv[direction][0] + x, conv[direction][1] + y

        if (x2 >= 0 and y2 >= 0 and x2 < n and y2 < n):
            if (state[x][y][direction] == 1):
                neighbours_list.append((x2, y2))

    return neighbours_list

def delete(state, x, y, direction):
    x2, y2 = conv[direction][0] + x, conv[direction][1] + y
    
    state[x][y][direction] = 1
    state[x2][y2][(2 + direction) % 4] = 1

def show(state, n, surface, wh, maxid):
    ratio = wh / n
    colors = {}
    
    for i in range(n):
        for j in range(n):
            for k in range(1, 3):
                mark = state[i][j][4]
                if mark in colors:
                    markColor = colors[mark]
                else:
                    if mark == maxid:
                        markColor = (255, 0, 0)
                    else:
                        markColor = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))
                    colors[mark] = markColor
                    
                i2, j2 = conv[k]
                i2, j2 = i + i2, j + j2

                if state[i][j][k] == 1:
                    pygame.draw.line(surface, colors[mark], (i * ratio, j * ratio), (i2 * ratio, j2 * ratio))

N = 100
probability = 0.5

network = []
initialize(network, N)
percolate(network, N, probability)

maxid = bfs_iterative(network, N)

pygame.init()

display = pygame.display.set_mode((700,700))
pygame.display.set_caption('Percolation Z2 simulator')

closed = False

display.fill((255,255,255))
show(network, N, display, 700, maxid)

pygame.display.update()

while not closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

pygame.quit()
