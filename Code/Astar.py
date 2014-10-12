import time
start = time.time()

###############################
#       DEFINITIONS
###############################

import sys
if len(sys.argv) == 2:
        filename = str(sys.argv[1])
else:
        print "\n\n ERROR: Please insert ONE labyrinth filename\n\n"
        exit()
        
#filename = 'inputTest1.txt'

CLOSED = 0
OPEN = 1

paths = []
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
	if number == 1:
		return ' '
	if number == 2:
	        return 'AGENT'
        if number == 3:
	        return 'FINISH'
        if number >= 100 and number <= 199:
                return 'SWIT'+`number-100`
        if number >= 200 and number <= 299:
                return 'CLOS'+`number-200`
        if number >= 300 and number <= 399:
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
#       Assumes that the agent is not in an edge of the lab
def successor(doors, lab, x, y, w, h):
        children = []
        if lab[x-1][y]!=0 and (lab[x-1][y] < 200 or doors[lab[x-1][y]%100][(x-1,y)] == OPEN):
                #print lab[x-1][y], doors[lab[x-1][y]%100]
                children.append('U')
        if lab[x+1][y]!=0 and (lab[x+1][y] < 200 or doors[lab[x+1][y]%100][(x+1,y)] == OPEN):
                children.append('D')
        if lab[x][y-1]!=0 and (lab[x][y-1] < 200 or doors[lab[x][y-1]%100][(x,y-1)] == OPEN):
                children.append('L')
        if lab[x][y+1]!=0 and (lab[x][y+1] < 200 or doors[lab[x][y+1]%100][(x,y+1)] == OPEN):
                children.append('R')
        if lab[x][y] >= 100 and lab[x][y] <= 199 and doors.get(lab[x][y]%100) != None:
                if not allopen(lab, lab[x][y]):
                        children.append('P')

        return children        

def getnewpos(movement, x, y):
        if movement == 'U':
                return [x-1, y]
        if movement == 'R':
                return [x, y+1]
        if movement == 'D':
                return [x+1, y]
        if movement == 'L':
                return [x, y-1]
        if movement == 'P':
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

# Next selected node based on heuristic
def SelectSucNode(paths):
        index = 0
        LowerF = paths[0].hFunc + paths[0].gFunc
        if len(paths) > 1:
                for i in range(1, len(paths)):
                        if (paths[i].hFunc + paths[i].gFunc) < LowerF:
                                LowerF = (paths[i].hFunc + paths[i].gFunc)
                                index = i
        return index 

#Heuristic Computation - Manhattan Distance
def ComputeHeuristicManhattan(xfinish,yfinish,x,y):
        return (abs(xfinish - x) + abs(yfinish - y))

                           
###############################
#       MAIN
###############################

# Store numbers from file in lab        
with open(filename) as f:
    h, w = [int(x) for x in f.readline().split()] # read first line
    lab = []
    for line in f: # read rest of lines
        lab.append([int(x) for x in line.split()])
        
printlab(lab, w, h)

# init paths list
[x, y] = search_ipos(lab, w, h, 2) # look for agent
[xfinish, yfinish] = search_ipos(lab, w, h, 3) # look for finish

doors = Ncreate_doors_dict(lab, w, h)
heuristic = ComputeHeuristicManhattan(xfinish,yfinish,x,y)
isuccessors = successor(doors, lab, x, y, w, h)

for i in range(0, len(isuccessors)):
        [newx, newy] = getnewpos(isuccessors[i], x, y)
        auxpath = path(isuccessors[i], newx, newy, x, y, doors,1,ComputeHeuristicManhattan(xfinish,yfinish,newx,newy))
        paths.append(auxpath)

# do the search
depth = 0
solved = 0
GeneratedNodes = len(paths);

while paths and not solved:
        index2rem = []
        
        #Select succesor node based on MIN_f = g + h
        i = SelectSucNode(paths)

        
        # save elements
        name = paths[i].name
        x = paths[i].x
        y = paths[i].y
        prevx = paths[i].prevx
        prevy = paths[i].prevy
        doors = dict(paths[i].doors)
        g = paths[i].gFunc 
        # compute possible movements
        succ = successor(paths[i].doors, lab, x, y, w, h)
        depth = len(paths[i].name)
        for j in range(0, len(succ)):
                [newx, newy] = getnewpos(succ[j], x, y)
                # Check if labyrinth is solved
                if newx == xfinish and newy == yfinish and not solved:
                        print 'LABYRINTH IS SOLVED'
                        solved = 1
                        name += succ[j]
                        #print 'X: ',newx,'Y: ',newy,'H: ',paths[i].hFunc,'G: ',paths[i].gFunc
                        print 'Number of Steps: ',len(name)
                        print 'Solution Steps: ',name
                if not solved and (newx != prevx or newy != prevy):#Lets generate successor nodes
                        GeneratedNodes += 1;
                        if len(paths[i].name) == depth:
                                paths[i].name += succ[j]
                                paths[i].prevx = x
                                paths[i].prevy = y
                                paths[i].x = newx
                                paths[i].y = newy
                                                    
                                paths[i].hFunc = ComputeHeuristicManhattan(xfinish,yfinish,newx,newy)
                                  
                                
                                if succ[j] == 'P':
                                        doorsaux = {list(doors.keys())[i]: dict(doors.values()[i]) for i in range(len(doors.keys()))}
                                        for var in doorsaux[lab[x][y]%100]:
                                                doorsaux[lab[x][y]%100][var] = 1-doorsaux[lab[x][y]%100][var]
                                        paths[i].doors = dict(doorsaux)
                                        paths[i].gFunc = g
                                else:
                                        paths[i].gFunc += 1
                        
                        else:
                                doorsaux = {list(doors.keys())[i]: dict(doors.values()[i]) for i in range(len(doors.keys()))}
                                if succ[j] == 'P':
                                        for var in doorsaux[lab[x][y]%100]:
                                                doorsaux[lab[x][y]%100][var] = 1-doorsaux[lab[x][y]%100][var]
                                        gaux = g
                                else:
                                        gaux = g+1        
                                auxpath = path(name+succ[j], newx, newy, x, y, doorsaux,gaux,ComputeHeuristicManhattan(xfinish,yfinish,x,y))
                                paths.append(auxpath)

        if len(paths[i].name) == depth:
                index2rem.append(i)
        
        
        #remove repetitions with more steps if exist
        for z in range(len(paths)):
                for y in range(z+1, len(paths)):
                        if paths[z].x == paths[y].x and paths[z].y == paths[y].y and paths[z].doors == paths[y].doors:
                                if len(paths[z].name)>len(paths[y].name):
                                        remove = z
                                else:
                                        remove = y
                                if y not in index2rem:
                                        index2rem.append(remove)



                                        
                
        # remove selected paths
        index2rem = sorted(index2rem)
        for k in range(0, len(index2rem)):
                paths.pop(index2rem[k]-k)


          
if not solved:
        print 'Problem does not have a solution'   
end = time.time()
print 'Generated Nodes: ', GeneratedNodes
print 'Execution time: ', end-start, 'seconds'
