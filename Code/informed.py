import time
start = time.time()

time1 = 0

import sys
import os.path
import copy

###############################
#       DEFINITIONS
###############################

import sys
if len(sys.argv) == 2:
        filename = str(sys.argv[1])
else:
        print "\n\n ERROR: Please insert ONE labyrinth filename\n\n"
        exit()
        
#filename = 'inputTest6.txt'

CLOSED = 0
OPEN = 1


class path:
        def __init__(self, name, x, y, prevx, prevy, doors,gFunc,hFunc):
                self.name  = name
                self.x     = x
                self.y     = y
                self.prevx = prevx
                self.prevy = prevy
                self.doors = doors
                self.gFunc = gFunc
                self.hFunc = hFunc
                
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
# Prints Solution
def SOLUTION(path2solution):
    print 'LABYRINTH IS SOLVED'
    print 'Number of Steps: ',len(path2solution)
    print 'Solution Steps: ',path2solution  

# Next selected node based on heuristic
def SelectSucNode(node):
        index = 0
        LowerF = node[0].hFunc + node[0].gFunc
        if len(node) > 1:
                for i in range(1, len(node)):
                        if (node[i].hFunc + node[i].gFunc) < LowerF:
                                LowerF = (node[i].hFunc + node[i].gFunc)
                                index = i
        return index
 

#Heuristic Computation - Manhattan Distance
def ComputeHeuristicManhattan(xfinish,yfinish,x,y):
        return (abs(xfinish - x) + abs(yfinish - y))

                           
###############################
#       MAIN
###############################
solved = False
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
        
printlab(lab, w, h)

[x, y] = search_ipos(lab, w, h, 2) # look for agent
[xfinish, yfinish] = search_ipos(lab, w, h, 3) # look for finish

doors = Ncreate_doors_dict(lab, w, h)
g = 0
h = ComputeHeuristicManhattan(xfinish,yfinish,x,y)
isuccessors = successor(doors, lab, x, y, w, h)

# init explored and frontier
explored = []
frontier = []
if x != xfinish or y != yfinish:
    frontier.append(path('', x, y, x, y, doors, g,h))
else:
    solved = True
    SOLUTION('')

# do the search
GeneratedNodes = len(frontier)
index = 0
while frontier and not solved:

    #Select succesor node based on MIN_f = g + h
    index = SelectSucNode(frontier)

    # save elements
    name = frontier[index].name
    x = frontier[index].x
    y = frontier[index].y
    prevx = frontier[index].prevx
    prevy = frontier[index].prevy
    doors = dict(frontier[index].doors)
    gFunc = frontier[index].gFunc 
    
    succ = successor(doors, lab, x, y, w, h)
    
    explored.append(frontier[index])
    frontier.pop(index)
    
    #Evaluate and Generate Child Nodes        
    for j in range(len(succ)):
        [newx, newy] = getnewpos(succ[j], x, y)
        # Check if labyrinth is solved
        if newx == xfinish and newy == yfinish and not solved:
            solved = True
            name += succ[j]
            SOLUTION(name)
        if not solved and (newx != prevx or newy != prevy):
            GeneratedNodes += 1;
                             
            doorsaux = copy.deepcopy(doors)
            g = gFunc+1
            h = ComputeHeuristicManhattan(xfinish,yfinish,newx,newy)
            if succ[j] == 'P':
                for var in doorsaux[lab[newx][newy]%100]:
                    doorsaux[lab[newx][newy]%100][var] = 1-doorsaux[lab[newx][newy]%100][var]
            auxpath = path(name+succ[j], newx, newy, x, y, doorsaux,g,h)
            
            # check if auxpath is in explored or frontier
            add = 1
                       
            for b in range(len(explored)):
                if auxpath.x == explored[b].x and auxpath.y == explored[b].y and auxpath.doors == explored[b].doors:
                    add = 0
                    break

            if add:
                for a in range(len(frontier)):
                    if auxpath.x == frontier[a].x and auxpath.y == frontier[a].y and auxpath.doors == frontier[a].doors:
                        add = 0
                        break
            
            if add:
                frontier.append(auxpath)
          
if not solved:
        print 'Problem does not have a solution'   
print 'Generated Nodes: ', GeneratedNodes
ElapsedTime = time.time() - start
print 'Execution time: ', ElapsedTime, 'seconds'
