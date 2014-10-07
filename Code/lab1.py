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

# searches for target's initial position (could be agent, finnish, etc.)
def search_ipos(lab, w, h, target):
        for line in range(0,h):
                for column in range(0,w):
                        if lab[line][column] == target:
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

# Opens door correspondent to given switch
def open_door(labaux, switch, w, h):
        door = switch + 100
        # find door position
        for l, row in enumerate(labaux):
                if door in row:
                        # open door
                        labaux[l][row.index(door)]+=100
                        break
        
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
[x, y] = search_ipos(lab, w, h, 2) # look for agent
[xfinnish, yfinnish] = search_ipos(lab, w, h, 3) # look for finnish

isuccessors = successor(lab, x, y, w, h)

for i in range(0, len(isuccessors)):
        [newx, newy] = getnewpos(isuccessors[i], x, y)
        auxpath = path(isuccessors[i], newx, newy, x, y, lab)
        paths.append(auxpath)

# do the search
depth = 0
solved = 0
while not solved:
        index2rem = []
        depth = depth+1
        for i in range(0, len(paths)):
                # save elements
                name = paths[i].name
                x = paths[i].x
                y = paths[i].y
                prevx = paths[i].prevx
                prevy = paths[i].prevy
                lab = [list(a) for a in paths[i].lab]
                # search for possible movements
                succ = successor(lab, x, y, w, h)
                for j in range(0, len(succ)):
                        [newx, newy] = getnewpos(succ[j], x, y)
                        # Check if labyrinth is solved
                        if newx == xfinnish and newy == yfinnish:
                                print 'LABYRINTH IS SOLVED'
                                solved = 1
                                paths[i].name += succ[j]
                                # Add all the other paths to the remove list
                                for s in range(0, len(paths)):
                                        if s != i:
                                                index2rem.append(s)
                        if not solved:
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
                                                open_door(paths[i].lab, lab[x][y], w, h)
                        #if paths[i].name == 'DDPUUUUURPLLLLLDDDDDRPLUUURRP':
                        #        print succ
                        #        printlab(paths[i].lab, w, h)
                if len(paths[i].name) == depth:
                        index2rem.append(i)
        # remove selected paths
        for k in range(0, len(index2rem)):
                if len(paths) == 1:
                        print '\nfinal:'
                        print len(paths[0].name)
                        print paths[0].name
                paths.pop(index2rem[k]-k)
        #if depth>30 and depth <= 35:
        #        print '---------'
        #        for d in range(0,len(paths)):
        #                print paths[d].name
print len(paths[0].name)
print paths[0].name
