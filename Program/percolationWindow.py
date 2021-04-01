import random
import pygame
from datetime import datetime
import os

conv = [(1, 0), (0, -1), (-1, 0), (0, 1)]
def initialize(state, n, value=1):
    state = []
    
    for i in range(n):
        state.append([]);
        for j in range(n):
            state[i].append([value, value, value, value, 0]) # RULD
    return state

def percolate(state, n, p):
    random.seed()
    
    for i in range(n):
        for j in range(n):
            for k in range(1, 3):
                if random.random() < p:
                    delete(state, (i, j), k)
    return state

def dfs_subexplore(state, n, point, mark):
    i, j = point
    state[i][j][4] = mark
         
    for neighbour in neighbours(state, n, point, 0):
        i2, j2 = neighbour
        if state[i2][j2][4] == 0:
            dfs_subexplore(state, n, neighbour, mark)

def dfs_explore(state, n):
    mark = 1
    
    for i in range(1, n):
        for j in range(1, n):
            s = (i, j)
            if state[i][j][4] == 0:
                mark += 1
                dfs_subexplore(state, n, s, mark)

def dfs_subiterative(state, n, point, mark):
    count = 0
    
    stack = []

    stack.append(point)
    while len(stack) != 0:
        point = stack.pop()
        i, j = point

        if state[i][j][4] == 0:
            state[i][j][4] = mark
            count += 1
            for neighbour in neighbours(state, n, point, 0):
                i2, j2 = neighbour
                stack.append(neighbour)

    return count

def dfs_iterative(state, n):
    mark = 1
    
    maxcount = -1
    maxid = -1
    
    for i in range(1, n):
        for j in range(1, n):
            s = (i, j)
            if state[i][j][4] == 0:
                mark += 1
                count = dfs_subiterative(state, n, s, mark)
                if count > maxcount:
                    maxcount = count
                    maxid = mark
    return maxid

def bfs_subiterative(state, n, point, mark):
    count = 0
    
    queue = []

    x, y = point
    state[x][y][4] = mark
    queue.append(point)

    while queue != []:
        v = queue.pop(0)
        i, j = v
        
        for neighbour in neighbours(state, n, v, 0):
            i2, j2 = neighbour
            
            if state[i2][j2][4] == 0:
                state[i2][j2][4] = mark
                count += 1
                
                queue.append(neighbour)

    return count

def bfs_iterative(state, n):
    mark = 1

    maxcount = -1
    maxid = -1
    
    for i in range(1, n):
        for j in range(1, n):
            s = (i, j)
            if state[i][j][4] == 0:
                mark += 1
                
                count = bfs_subiterative(state, n, s, mark)
                if count > maxcount:
                    maxcount = count
                    maxid = mark
    return maxid

def bfs_subexplore(state, queue, n, mark):
    if queue == []:
        return

    v = queue.pop(0)
    print(v)

    for neighbour in neighbours(state, n, v, 0):
        i, j = neighbour

        if state[i][j][4] == 0:
            state[i][j][4] = mark
            queue.append(neighbour)

    bfs_subexplore(state, queue, n, mark)

def bfs_explore(state, n):
    mark = 1
    
    for i in range(1, n):
        for j in range(1, n):
            s = (i, j)
            if state[i][j][4] == 0:
                mark += 1
                queue = [s]
                
                bfs_subexplore(state, queue, n, mark)

def neighbours(state, n, point, value=1):
    x, y = point

    neighbours_list = []
    
    for direction in range(4):
        x2, y2 = conv[direction]
        x2, y2 = x2 + x, y2 + y

        if (x2 >= 0 and y2 >= 0 and x2 < n and y2 < n):
            if (state[x][y][direction] == value):
                neighbours_list.append((x2, y2))

    return neighbours_list

def delete(state, point, direction):
    x, y = point
    
    x2, y2 = conv[direction]
    x2, y2 = x2 + x, y2 + y
    
    state[x][y][direction] = 0
    state[x2][y2][(2 + direction) % 4] = 0

    return state

def clearMarks(state, n):
    for i in range(n):
        for j in range(n):
            state[i][j][4] = 0

def show(state, n, surface, wh, maxid):
    random.seed(0)
    
    ratio = wh / n

    if showOpenClusters:
        colors = {}
    
    gray = (220,220,220)
    black = (0,0,0)

    delta = 0
    if isDual:
        delta += ratio / 2
    
    for i in range(n):
        for j in range(n):
            for k in range(1, 3):
                if showOpenClusters:
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

                if showOpenClusters:
                    if state[i][j][k] == 0:
                        pygame.draw.line(surface, gray, (i * ratio + delta, j * ratio + delta), (i2 * ratio + delta, j2 * ratio + delta))
                    else:
                        pygame.draw.line(surface, colors[mark], (i * ratio + delta, j * ratio + delta), (i2 * ratio + delta, j2 * ratio + delta))
                else:
                    if state[i][j][k] == 0:
                        pygame.draw.line(surface, black, (i * ratio + delta, j * ratio + delta), (i2 * ratio + delta, j2 * ratio + delta))

def updateSliders():
    pygame.draw.rect(gameDisplay, white, slidersBox)
    
    pygame.draw.rect(gameDisplay, black, sliderSzRectBox)
    sliderSzCircleBox = (sliderSzCircleCenterLocation[0] - sliderSzCircleRadius + ((N - minN) / (maxN - minN)) * sliderSzRectSize[0], sliderSzCircleCenterLocation[1] - sliderSzCircleRadius, 2 * sliderSzCircleRadius,  2 * sliderSzCircleRadius)
    pygame.draw.ellipse(gameDisplay, gray, sliderSzCircleBox)

    probabilityTextSurface = font.render("p = " + str(probability), False, (0, 0, 0))

    pygame.draw.rect(gameDisplay, black, sliderProbRectBox)
    sliderProbCircleBox = (sliderProbCircleCenterLocation[0] - sliderProbCircleRadius + probability * sliderProbRectSize[0], sliderProbCircleCenterLocation[1] - sliderProbCircleRadius, 2 * sliderProbCircleRadius,  2 * sliderProbCircleRadius)
    pygame.draw.ellipse(gameDisplay, gray, sliderProbCircleBox)
    
    sizeTextSurface = font.render("N = " + str(N), False, (0, 0, 0))
    
    gameDisplay.blit(sizeTextSurface, sizeTextLocation)
    gameDisplay.blit(probabilityTextSurface, probabilityTextLocation)
    
    pygame.display.update()

def updateAll():
    gameDisplay.fill(white)
    show(network, N, gameDisplay, box_wh, maxid)
    #pygame.draw.rect(gameDisplay, black, sliderProbRectBox)
    #sliderProbCircleBox = (sliderProbCircleCenterLocation[0] - sliderProbCircleRadius + probability * sliderProbRectSize[0], sliderProbCircleCenterLocation[1] - sliderProbCircleRadius, 2 * sliderProbCircleRadius,  2 * sliderProbCircleRadius)
    #pygame.draw.ellipse(gameDisplay, gray, sliderProbCircleBox)
    
    #probabilityTextSurface = font.render("p = " + str(probability), False, (0, 0, 0))
    
    updateSliders()
    
    gameDisplay.blit(buttonImage, buttonLocation)
    gameDisplay.blit(saveButtonImage, saveButtonLocation)
    gameDisplay.blit(dualButtonImage, dualButtonLocation)
    gameDisplay.blit(opClustersCheckboxImage, opClustersCheckboxLocation)
    
    gameDisplay.blit(openClustersSurface, openClustersTextLocation)
    #gameDisplay.blit(probabilityTextSurface, probabilityTextLocation)
    
    pygame.display.update()

def screenshot():
    now = datetime.now()
    strNow = now.strftime("%Y_%m_%d__%H_%M_%S")

    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        
    pygame.image.save(gameDisplay, "screenshots\\screenshot_" + strNow + ".png")

def dual(state, n):
    dual = []
    dual = initialize(dual, n, 0)
    for i in range(n):
        for j in range(n):
            
            if i + 1 < n and j + 1 < n:
                dual[i][j][0] = state[i + 1][j + 1][1]
                dual[i][j][3] = state[i + 1][j + 1][2]
            
            dual[i][j][1] = state[i][j][0]
            dual[i][j][2] = state[i][j][3]
    return dual

N = 200
maxN = 500
minN = 5

showOpenClusters = True

probability = 0.5

isDual = False

network = []
network = initialize(network, N)
network = percolate(network, N, probability)

network0 = network
dualNetwork = dual(network, N)

#dfs_subexplore(network, N, (60, 50), (50,50), 1)

if showOpenClusters:
    maxid = bfs_iterative(network, N)
else:
    maxid = -1

pygame.init()

display_width = 900
display_height = 700

box_wh = 700

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Percolation simulator')

black = (0,0,0)
white = (255,255,255)
gray = (128,128,128)

clock = pygame.time.Clock()
closed = False

gameDisplay.fill(white)
show(network, N, gameDisplay, box_wh, maxid)

buttonLocation = (725, 25)
buttonSize = (50, 50)
buttonSurface = pygame.Surface(buttonSize)
buttonImage = pygame.image.load("assets\\restartButton.png")

saveButtonLocation = (825, 25)
saveButtonSize = (50, 50)
saveButtonSurface = pygame.Surface(saveButtonSize)
saveButtonImage = pygame.image.load("assets\\saveButton.png")

dualButtonLocation = (825, 275)
dualButtonSize = (50, 50)
dualButtonSurface = pygame.Surface(dualButtonSize)
dualButtonImage = pygame.image.load("assets\\dualButton.png")

opClustersCheckboxLocation = (845, 200)
opClustersCheckboxSize = (30, 30) 
opClustersCheckboxState = True

if opClustersCheckboxState:
    opClustersCheckboxImage = pygame.image.load("assets\\checked.png")
else:
    opClustersCheckboxImage = pygame.image.load("assets\\unchecked.png")

sliderProbRectLocation = (725, 100)
sliderProbRectSize = (150, 2)
sliderProbRectBox = (sliderProbRectLocation[0], sliderProbRectLocation[1], sliderProbRectSize[0], sliderProbRectSize[1])
#sliderRect = pygame.Surface(sliderRectBox)

sliderProbCircleCenterLocation = (725, 100)
sliderProbCircleRadius = 5
sliderProbDraging = False

sliderSzRectLocation = (725, 150)
sliderSzRectSize = (150, 2)
sliderSzRectBox = (sliderSzRectLocation[0], sliderSzRectLocation[1], sliderSzRectSize[0], sliderSzRectSize[1])

sliderSzCircleCenterLocation = (725, 150)
sliderSzCircleRadius = 5

sliderSzDraging = False
slidersBox = (700, 80, 200, 100)

font = pygame.font.SysFont('Arial', 13)

probabilityTextLocation = (750, 115)
probabilityTextSurface = font.render("p = " + str(probability), False, (0, 0, 0))

sizeTextLocation = (750, 165)
sizeTextSurface = font.render("N = " + str(N), False, (0, 0, 0))

openClustersTextLocation = (740, 207)
openClustersSurface = font.render("Show open clusters", False, (0, 0, 0))

pygame.draw.rect(gameDisplay, black, sliderProbRectBox)
sliderProbCircleBox = (sliderProbCircleCenterLocation[0] - sliderProbCircleRadius + probability * sliderProbRectSize[0], sliderProbCircleCenterLocation[1] - sliderProbCircleRadius, 2 * sliderProbCircleRadius,  2 * sliderProbCircleRadius)
pygame.draw.ellipse(gameDisplay, gray, sliderProbCircleBox)

pygame.draw.rect(gameDisplay, black, sliderSzRectBox)
sliderSzCircleBox = (sliderSzCircleCenterLocation[0] - sliderSzCircleRadius + ((N - minN) / (maxN - minN)) * sliderSzRectSize[0], sliderSzCircleCenterLocation[1] - sliderSzCircleRadius, 2 * sliderSzCircleRadius,  2 * sliderSzCircleRadius)
pygame.draw.ellipse(gameDisplay, gray, sliderSzCircleBox)

gameDisplay.blit(buttonImage, buttonLocation)
gameDisplay.blit(saveButtonImage, saveButtonLocation)
gameDisplay.blit(dualButtonImage, dualButtonLocation)
gameDisplay.blit(opClustersCheckboxImage, opClustersCheckboxLocation)
gameDisplay.blit(probabilityTextSurface, probabilityTextLocation)
gameDisplay.blit(sizeTextSurface, sizeTextLocation)
gameDisplay.blit(openClustersSurface, openClustersTextLocation)
           
pygame.display.update()

while not closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonLocation[0] <= mouse[0] <= buttonLocation[0] + buttonSize[0] and buttonLocation[1] <= mouse[1] <= buttonLocation[1] + buttonSize[1]: 
                network = []
                network = initialize(network, N)
                network = percolate(network, N, probability)
                                
                network0 = network
                dualNetwork = dual(network, N)

                if showOpenClusters:
                    maxid = bfs_iterative(network, N)
                else:
                    maxid = -1
                
                updateAll()
            
            if saveButtonLocation[0] <= mouse[0] <= saveButtonLocation[0] + saveButtonSize[0] and saveButtonLocation[1] <= mouse[1] <= saveButtonLocation[1] + saveButtonSize[1]: 
                screenshot()

            if dualButtonLocation[0] <= mouse[0] <= dualButtonLocation[0] + dualButtonSize[0] and dualButtonLocation[1] <= mouse[1] <= dualButtonLocation[1] + dualButtonSize[1]: 
                if not isDual:
                    network = dualNetwork
                else:
                    network = network0
                isDual = not isDual
                updateAll()
    
            if opClustersCheckboxLocation[0] <= mouse[0] <= opClustersCheckboxLocation[0] + opClustersCheckboxSize[0] and opClustersCheckboxLocation[1] <= mouse[1] <= opClustersCheckboxLocation[1] + opClustersCheckboxSize[1]: 
                opClustersCheckboxState = not opClustersCheckboxState
                showOpenClusters = opClustersCheckboxState
                
                if opClustersCheckboxState:
                    opClustersCheckboxImage = pygame.image.load("assets\\checked.png")
                else:
                    opClustersCheckboxImage = pygame.image.load("assets\\unchecked.png")

                if showOpenClusters and maxid == -1:
                    maxid = bfs_iterative(network, N)
                    
                updateAll()
                                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sliderProbRectLocation[0] <= mouse[0] <= sliderProbRectLocation[0] + sliderProbRectSize[0] and sliderProbRectLocation[1] - 10 <= mouse[1] <= sliderProbRectLocation[1] + 10:
                x, y = event.pos
                
                probability = (x - sliderProbRectLocation[0]) / sliderProbRectSize[0]
                updateSliders()
                                
                sliderProbDraging = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if sliderSzRectLocation[0] <= mouse[0] <= sliderSzRectLocation[0] + sliderSzRectSize[0] and sliderSzRectLocation[1] - 10 <= mouse[1] <= sliderSzRectLocation[1] + 10:
                x, y = event.pos
                
                N = int((x - sliderSzRectLocation[0]) / sliderSzRectSize[0] * (maxN - minN)) + minN
                updateSliders()
                                
                sliderSzDraging = True
            
        if event.type == pygame.MOUSEBUTTONUP:
            #if sliderRectLocation[0] <= mouse[0] <= sliderRectLocation[0] + sliderRectSize[0] and sliderRectLocation[1] - 10 <= mouse[1] <= sliderRectLocation[1] + 10:
            sliderProbDraging = False
            sliderSzDraging = False
            
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            
            if sliderProbDraging and sliderProbRectLocation[0] <= x <= sliderProbRectLocation[0] + sliderProbRectSize[0]:
                probability = (x - sliderProbRectLocation[0]) / sliderProbRectSize[0]
                updateSliders()
            
            if sliderSzDraging and sliderSzRectLocation[0] <= x <= sliderSzRectLocation[0] + sliderSzRectSize[0]:
                N = int((x - sliderSzRectLocation[0]) / sliderSzRectSize[0] * (maxN - minN)) + minN
                updateSliders()
        if event.type == pygame.KEYDOWN:
            if sliderSzDraging:
                if event.key == pygame.K_LEFT:
                    N -= 1
                if event.key == pygame.K_RIGHT:
                    N += 1
                    
                if N > maxN:
                    N = maxN
                elif N < minN:
                    N = minN
                updateSliders()
        

    mouse = pygame.mouse.get_pos()
    clock.tick(60)

pygame.quit()
exit()
