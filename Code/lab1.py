filename = 'input_example.txt'

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
