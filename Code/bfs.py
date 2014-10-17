import time
start = time.time()

import sys
import os.path
import copy

###############################
#       DEFINITIONS
###############################

CLOSED = 0
OPEN = 1

class path:
    def __init__(self, name, x, y, prevx, prevy, doors):
        self.name  = name
        self.x     = x
        self.y     = y
        self.prevx = prevx
        self.prevy = prevy
        self.doors = doors
            
###############################
#       FUNCTIONS
###############################

# Decodes number from file to print in a more human readable way
def labdecode(number):
    if number == 0:
        return '[[[]]]'
    elif number == 1:
        return ' '
    elif number == 2:
        return 'AGENT'
    elif number == 3:
        return 'FINISH'
    elif number >= 100 and number <= 199:
        return 'SWIT'+`number-100`
    elif number >= 200 and number <= 299:
        return 'CLOS'+`number-200`
    elif number >= 300 and number <= 399:
        return 'OPEN'+`number-300`
    return number      

# Prints labyrinth  
def printlab(lab, w, h):
    for line in range(0,h):
        for column in range(0,w):
            print labdecode(lab[line][column]),'\t',
        print '\n'        

# searches for target's initial position (could be agent, finish, etc.)
def search_ipos(lab, w, h, target):
    for line in range(0,h):
        for column in range(0,w):
            if lab[line][column] == target:
                return [line, column]         
        
# Successor function: given a node, returns the set of child nodes
#   Assumes that the agent is not in an edge of the lab
def successor(doors, lab, x, y, w, h):
    children = []
    U = lab[x-1][y]
    D = lab[x+1][y]
    L = lab[x][y-1]
    R = lab[x][y+1]
    P = lab[x][y]
    if U != 0 and (U < 200 or doors[U % 100][(x-1,y)] == OPEN):
        children.append('U')
    if D != 0 and (D < 200 or doors[D % 100][(x+1,y)] == OPEN):
        children.append('D')
    if L != 0 and (L < 200 or doors[L % 100][(x,y-1)] == OPEN):
        children.append('L')
    if R != 0 and (R < 200 or doors[R % 100][(x,y+1)] == OPEN):
        children.append('R')
    if P >= 100 and P <= 199 and doors.get(P % 100) != None:
        if not allopen(lab, P):
            children.append('P')

    return children        

# Computes new position from given movement
def getnewpos(movement, x, y):
    if movement == 'U':
        return [x-1, y]
    elif movement == 'R':
        return [x, y+1]
    elif movement == 'D':
        return [x+1, y]
    elif movement == 'L':
        return [x, y-1]
    elif movement == 'P':
        return [x, y]

# Checks if door correspondent to given switch is closed
def allopen(lab, switch):
    var = 1
    for x in doors[switch%100].values():
        var *= x
    return var
        
# Create doors dictionary
def Ncreate_doors_dict(lab, w, h):
    dic = {}
    for line in range(0,h):
        for column in range(0,w):
            if lab[line][column]>=200 and lab[line][column]<=299:
                if lab[line][column]%100 in dic:
                    dic[lab[line][column]%100][(line,column)] = CLOSED
                else:
                    dic[lab[line][column]%100] = {(line,column):CLOSED}            
            if lab[line][column]>=300 and lab[line][column]<=399:
                if lab[line][column]%100 in dic:
                    dic[lab[line][column]%100][(line,column)] = OPEN
                else:
                    dic[lab[line][column]%100] = {(line,column):OPEN}      
    return dic
    
# Breadth-First-Search algorythm
def bfs(lab, doors, x, y, w, h, xfinish, yfinish):
    solved = False

    # init explored and frontier
    explored = []
    frontier = []
    if x != xfinish or y != yfinish:
        frontier.append(path('', x, y, x, y, doors))
    else:
        name = ''
        solved = True

    # do the search
    GeneratedNodes = len(frontier)
    while frontier and not solved:
        # save elements
        name = frontier[0].name
        x = frontier[0].x
        y = frontier[0].y
        prevx = frontier[0].prevx
        prevy = frontier[0].prevy
        doors = dict(frontier[0].doors)
        succ = successor(doors, lab, x, y, w, h)
        
        explored.append(frontier[0])
        frontier.pop(0)
        
        for j in range(len(succ)):
            [newx, newy] = getnewpos(succ[j], x, y)
            # Check if labyrinth is solved
            if newx == xfinish and newy == yfinish and not solved:
                name += succ[j]
                solved = True
                
            if not solved and (newx != prevx or newy != prevy):
                GeneratedNodes += 1
                
                doorsaux = copy.deepcopy(doors)
                
                if succ[j] == 'P':
                    sval = lab[newx][newy]
                    for var in doorsaux[sval%100]:
                        doorsaux[sval%100][var] = 1-doorsaux[sval%100][var]
                
                # check if auxpath is in explored or frontier
                add = 1
                for a in range(len(explored)):
                    if newx == explored[a].x and newy == explored[a].y and doorsaux == explored[a].doors:
                        add = 0
                        break
                if add:
                    for a in range(len(frontier)):
                        if newx == frontier[a].x and newy == frontier[a].y and doorsaux == frontier[a].doors:
                            add = 0
                            break
                if add:
                    frontier.append(path(name+succ[j], newx, newy, x, y, doorsaux))

    return [solved, GeneratedNodes, name]

                      
###############################
#       MAIN
###############################

# Read file from terminal
if len(sys.argv) == 2 and os.path.isfile(str(sys.argv[1])):
        filename = str(sys.argv[1])
else:
        print "ERROR: Please insert ONE valid labyrinth filename."
        exit()

# Store numbers from file in lab        
with open(filename) as f:
    h, w = [int(x) for x in f.readline().split()] # read first line
    lab = []
    for line in f: # read rest of lines
        lab.append([int(x) for x in line.split()])

# Print labyrinth in the terminal       
printlab(lab, w, h)

[x, y] = search_ipos(lab, w, h, 2) # look for agent
[xfinish, yfinish] = search_ipos(lab, w, h, 3) # look for finish

doors = Ncreate_doors_dict(lab, w, h)

# Breadth-First-Search
[solved, GeneratedNodes, name] = bfs(lab, doors, x, y, w, h, xfinish, yfinish)

if solved:
    print 'LABYRINTH IS SOLVED'
    print 'Number of Steps: ', len(name)
    print 'Solution Steps: ', name
else:
    print 'Problem does not have a solution'   
         
ElapsedTime = time.time() - start
print 'Generated Nodes: ', GeneratedNodes
print 'Execution time: ', ElapsedTime, 'seconds'

