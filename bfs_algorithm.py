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
