import time
start = time.time()

###############################
#       DEFINITIONS
###############################
#
import sys
if len(sys.argv) == 2:
        filename = str(sys.argv[1])
else:
        print "\n\n ERROR: Please insert ONE labyrinth filename\n\n"
        exit()


#filename = 'inputTest7.txt'
CLOSED = 0
OPEN = 1

paths = []
class path:
        def __init__(self, name, x, y, prevx, prevy, doors,loop):
                self.name  = name
                self.x     = x
                self.y     = y
                self.prevx = prevx
                self.prevy = prevy
                self.doors = doors
                self.loop = loop
                
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

# searches for target's initial position (could be agent, finnish, etc.)
def search_ipos(lab, w, h, target):
        for line in range(0,h):
                for column in range(0,w):
                        if lab[line][column] == target:
                                return [line, column]         
        
# Successor function: given a node, returns the set of child nodes
#       Assumes that the agent is not in an edge of the lab
def successor(loop,doors, lab, x, y, w, h):
        #loop_thershold = 10
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
        

        #if in loop: no sucessors are passed and node is erased in main
        #try:
        #        loop[(x,y)] += 1                
        #        if loop[(x,y)] > loop_thershold:
        #                children = []
        #except KeyError:
        #        pass               
        

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

def iftest(var,test_value):
        if var > test_value:
                return 1
        else:
                return 0

#Create Possible Loop positions dictionary
def loop_avoid_dict(lab,w,h):
        dic = {}
        for line in range(0,h):
                for column in range(0,w):
                        sum = 0
                        if lab[line][column] > 0:
                                sum = iftest(lab[line-1][column],0)+iftest(lab[line+1][column],0)+iftest(lab[line][column-1],0)+iftest(lab[line][column+1],0)
                                if sum > 2:
                                        dic[(line,column)] = 0
        return dic                      
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
#print 'DICTIO: ', Ncreate_doors_dict(lab, w, h)
# init paths list
[x, y] = search_ipos(lab, w, h, 2) # look for agent
[xfinnish, yfinnish] = search_ipos(lab, w, h, 3) # look for finnish

doors = Ncreate_doors_dict(lab, w, h)
loop = loop_avoid_dict(lab,w,h)
isuccessors = successor(loop,doors, lab, x, y, w, h)

#print 'Initial loop state: ', loop

for i in range(len(isuccessors)):
        [newx, newy] = getnewpos(isuccessors[i], x, y)
        auxpath = path(isuccessors[i], newx, newy, x, y, doors,loop)
        paths.append(auxpath)

# do the search
depth = 0
solved = 0
GeneratedNodes = len(paths);
while paths and not solved:
        index2rem = []
        depth = depth+1
        for i in range(len(paths)):
                # save elements
                name = paths[i].name
                x = paths[i].x
                y = paths[i].y
                prevx = paths[i].prevx
                prevy = paths[i].prevy
                doors = dict(paths[i].doors)
                loop = dict(paths[i].loop)
                succ = successor(loop,paths[i].doors, lab, x, y, w, h)
                for j in range(len(succ)):
                        [newx, newy] = getnewpos(succ[j], x, y)
                        # Check if labyrinth is solved
                        if newx == xfinnish and newy == yfinnish:
                                print 'LABYRINTH IS SOLVED'
                                solved = 1
                                paths[i].name += succ[j]
                                print 'Number of Steps: ',len(paths[i].name)
                                print 'Solution Steps: ',paths[i].name
                                #print 'Final loop state: ',paths[i].loop
                        if not solved and (newx != prevx or newy != prevy):#Lets generate successor nodes
                                        GeneratedNodes += 1;
                                        if len(paths[i].name) == depth:
                                                paths[i].name += succ[j]
                                                paths[i].prevx = x
                                                paths[i].prevy = y
                                                paths[i].x = newx
                                                paths[i].y = newy
                                                paths[i].loop = loop
                                                if succ[j] == 'P':
                                                        doorsaux = {list(doors.keys())[i]: dict(doors.values()[i]) for i in range(len(doors.keys()))}
                                                        for var in doorsaux[lab[x][y]%100]:
                                                                doorsaux[lab[x][y]%100][var] = 1-doorsaux[lab[x][y]%100][var]
                                                        paths[i].doors = dict(doorsaux)                                                        
                                                                                                               
                                        else:
                                                doorsaux = {list(doors.keys())[i]: dict(doors.values()[i]) for i in range(len(doors.keys()))}
                                                if succ[j] == 'P':
                                                        for var in doorsaux[lab[x][y]%100]:
                                                                doorsaux[lab[x][y]%100][var] = 1-doorsaux[lab[x][y]%100][var]
                                                auxpath = path(name+succ[j], newx, newy, x, y, doorsaux,loop)
                                                paths.append(auxpath)                
                if len(paths[i].name) == depth:
                        index2rem.append(i)
                        
        # remove repetitions
        for z in range(len(paths)):
            for y in range(z+1, len(paths)):
                if paths[z].x == paths[y].x and paths[z].y == paths[y].y and paths[z].doors == paths[y].doors:
                    if y not in index2rem:
                        index2rem.append(y)
        # remove selected paths
        index2rem = sorted(index2rem)
        for k in range(len(index2rem)):
                #if len(paths) == 1:
                #    print paths[0].name
                paths.pop(index2rem[k]-k)

if paths == []:
        print 'Problem does not have a solution'        
end = time.time()
print 'Generated Nodes: ', GeneratedNodes
print 'Execution time: ', end-start, 'seconds'

