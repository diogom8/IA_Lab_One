###############################
#       DEFINITIONS
###############################

filename = 'input_example.txt'

paths = []
class path:
        def __init__(self, name, x, y, prevx, prevy, lab):
                self.name  = name
                self.x     = x
                self.y     = y
                self.prevx = prevx
                self.prevy = prevy
                self.lab   = lab      

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

# searches for agent's initial position
def search_ipos(lab, w, h):
        for line in range(0,h):
                for column in range(0,w):
                        if lab[line][column] == 2:
                                return [line, column]         
        
# Successor function: given a node, returns the set of child nodes
#       Assumes that the agent is not in an edge of the lab
def successor(lab, x, y, w, h):
        children = []
        if lab[x-1][y]!=0 and (lab[x-1][y]<200 or lab[x-1][y]>299):
                children.append('U')
        if lab[x+1][y]!=0and (lab[x+1][y]<200 or lab[x+1][y]>299):
                children.append('D')
        if lab[x][y-1]!=0 and (lab[x][y-1]<200 or lab[x][y-1]>299):
                children.append('L')
        if lab[x][y+1]!=0 and (lab[x][y+1]<200 or lab[x][y+1]>299):
                children.append('R')
        if lab[x][y] >= 100 and lab[x][y] <= 199:
                if isclosed(lab, lab[x][y]):
                        children.append('P')
        return children        

def getnewpos(lab, movement, x, y):
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

# Opens door correspondent to given switch
def open_door(labaux, switch, w, h):
        door = switch + 100
        # find door position
        for l, row in enumerate(labaux):
                if door in row:
                        # open door
                        labaux[l][row.index(door)]+=100
                        break
        return labaux
# Checks if door correspondent to given switch is closed
def isclosed(lab, switch):
        door = switch + 100
        # find door position
        for l, row in enumerate(lab):
                if door in row:
                        return True
        return False
     
###############################
#       MAIN
###############################

# Store numbers from file in lab        
with open(filename) as f:
    w, h = [int(x) for x in f.readline().split()] # read first line
    lab = []
    for line in f: # read rest of lines
        lab.append([int(x) for x in line.split()])
        
printlab(lab, w, h)

# init paths list
[x, y] = search_ipos(lab, w, h)

isuccessors = successor(lab, x, y, w, h)

for i in range(0, len(isuccessors)):
        [newx, newy] = getnewpos(lab, isuccessors[i], x, y)
        auxpath = path(isuccessors[i], newx, newy, x, y, lab)
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
                lab = paths[i].lab
                succ = successor(lab, x, y, w, h)
                for j in range(0, len(succ)):
                        [newx, newy] = getnewpos(lab, succ[j], x, y)
                        if newx != prevx or newy != prevy:
                                if len(paths[i].name) == depth:
                                        paths[i].name += succ[j]
                                        paths[i].prevx = x
                                        paths[i].prevy = y
                                        paths[i].x = newx
                                        paths[i].y = newy
                                else:
                                        auxpath = path(name+succ[j], newx, newy, x, y, lab)
                                        paths.append(auxpath)
                                if succ[j] == 'P':
                                        paths[i].lab = open_door(lab, lab[x][y], w, h)
                if len(paths[i].name) == depth:
                        index2rem.append(i)
        # remove paths with dead ends
        for k in range(0, len(index2rem)):
                if len(paths) == 1:
                        #print 'final:'
                        print len(paths[0].name)
                        print paths[0].name
                paths.pop(index2rem[k]-k)
#        if depth == 20:
#                for k in range(0, len(paths)):
#                        print paths[k].name
#                paths = []
