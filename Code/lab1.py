###############################
#       DEFINITIONS
###############################

filename = 'input_example.txt'

paths = []
class path:
        def __init__(self, name, x, y, prevx, prevy):
                self.name  = name
                self.x     = x
                self.y     = y
                self.prevx = prevx
                self.prevy = prevy       

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
def printlab(array, w, h):
        for line in range(0,h):
                for column in range(0,w):
                        print labdecode(array[line][column]),'\t',
                print '\n'        

# searches for agent's initial position
def search_ipos(array, w, h):
        for line in range(0,h):
                for column in range(0,w):
                        if array[line][column] == 2:
                                return [line, column]         
        
# Successor function: given a node, returns the set of child nodes
#       Assumes that the agent is not in an edge of the map
def successor(array, x, y, w, h):
        children = []
        if array[x-1][y]!=0 and (array[x-1][y]<200 or array[x-1][y]>299):
                children.append('U')
        if array[x+1][y]!=0and (array[x+1][y]<200 or array[x+1][y]>299):
                children.append('D')
        if array[x][y-1]!=0 and (array[x][y-1]<200 or array[x][y-1]>299):
                children.append('L')
        if array[x][y+1]!=0 and (array[x][y+1]<200 or array[x][y+1]>299):
                children.append('R')
        if array[x][y] >= 100 and array[x][y] <= 199:
                # TODO: CHECK IF DOOR IS CLOSED. AGENT SHOULD NEVER CLOSE A DOOR
                children.append('P')
        return children        

def getnewpos(array, movement, x, y):
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
                       
###############################
#       MAIN
###############################

# Store numbers from file in array        
with open(filename) as f:
    w, h = [int(x) for x in f.readline().split()] # read first line
    array = []
    for line in f: # read rest of lines
        array.append([int(x) for x in line.split()])
        
printlab(array, w, h)

# init paths list
[x, y] = search_ipos(array, w, h)

isuccessors = successor(array, x, y, w, h)

for i in range(0, len(isuccessors)):
        [newx, newy] = getnewpos(array, isuccessors[i], x, y)
        auxpath = path(isuccessors[i], newx, newy, x, y)
        paths.append(auxpath)

# do the search
# TODO: DO NOT LET PRESS TWICE IN A ROW
depth = 0
while(paths!=[]):
        index2rem = []
        depth = depth+1
        ilenpaths = len(paths) # because paths length changes while iterating
        for i in range(0, ilenpaths):
                name = paths[i].name
                x = paths[i].x
                y = paths[i].y
                prevx = paths[i].prevx
                prevy = paths[i].prevy
                succ = successor(array, x, y, w, h)
                for j in range(0, len(succ)):
                        [newx, newy] = getnewpos(array, succ[j], x, y)
                        if newx != prevx or newy != prevy:
                                if len(paths[i].name) == depth:
                                        paths[i].name += succ[j]
                                        paths[i].prevx = x
                                        paths[i].prevy = y
                                        paths[i].x = newx
                                        paths[i].y = newy
                                else:
                                        auxpath = path(name+succ[j], newx, newy, x, y)
                                        paths.append(auxpath)
                if len(paths[i].name) == depth:
                        index2rem.append(i)
        # remove paths with dead ends
        for k in range(0, len(index2rem)):
                if len(paths) == 1:
                        print 'final:'
                        print paths[0].name
                paths.pop(index2rem[k]-k)
