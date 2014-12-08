from cnf_converter_rules import *
from cnf_converter_auxiliary import *
import sys
import copy
import StringIO

#filename = 'input-example-3.txt'

###############################
#       FUNCTIONS             #
###############################

# reads a list of tuples from file
def readfile(filename):
    try:
        with open(filename) as f:
            sentences = []
            for line in f:
                try:
                    sentences.append(eval(line))
                except:
                    print 'Invalid line on File'
                    quit()
    except IOError:
        print 'ERROR: File "' + filename + '" does not exist!'
        quit()
    return sentences

# convert to cnf
def cnf(sentence):
    
    sentence = eliminate_implications(sentence)
    sentence = move_not_inwards(sentence)
    sentence = distribute(sentence)
    #Conversion to list of disjunctions
    clausesList,NliteralsBefore = convert2list(sentence)
    clausesList = simplify(clausesList,NliteralsBefore,'3')
    return clausesList

def getKey(item):
    return len(item)

# Resolution loop
def ResolutionLoop(UNION):
    NewClauses = True
    while(NewClauses):
        NewClauses = False
        #unit preference heuristic
        UNION.sort(key = getKey)
        
        NumberOfLiterals = countLiterals(UNION)
        for i in range(NumberOfLiterals):
            for j in range(i+1,len(UNION)):
                result = resolution(UNION[i],UNION[j])
                if result != [UNION[i],UNION[j]]:
                    if result == set([]):
                        return True
                    else: #Result is some new conclusion
                        UNION.pop(j)
                        UNION.insert(j,result)
                        NewClauses = True
                        break
                    
            if NewClauses:
                break             
    return False

# Resolution loop - Step by Step
def ResolutionLoopSbS(UNION):
    output = StringIO.StringIO()
    NewClauses = True
    while(NewClauses):
        NewClauses = False
        print >>output, 'Result:', los2lol(UNION), '\n'
        #unit preference heuristic
        print >>output, 'Apply Unit Preference Heuristic'
        UNION.sort(key = getKey)
        print >>output, 'Result:', los2lol(UNION), '\n'
        
        NumberOfLiterals = countLiterals(UNION)
        for i in range(NumberOfLiterals):
            for j in range(i+1,len(UNION)):
                print >>output, ("Apply Resolution - C%d + C%d" % (i+1,j+1))
                result = resolution(UNION[i],UNION[j])
                if result != [UNION[i],UNION[j]]:
                    if result == set([]):
                        print >>output, 'Result: [] \n'
                        print >>output, 'CONCLUSION: Sentence can be proven from KB\n'
                        return True, output
                    else: #Result is some new conclusion
                        UNION.pop(j)
                        UNION.insert(j,result)
                        NewClauses = True
                        break
                print >>output, 'Result:', los2lol(UNION), '\n'
                
            if NewClauses:
                break
    print >>output, 'CONCLUSION: Sentence can\'t be proven from KB\n'             
    return False, output

# Count number of literals in UNION
def countLiterals(UNION):
    SUM = 0
    for item in UNION:
        if len(item) == 1:
            SUM += 1
    return SUM

# Resolution algorithm   
def resolution(X,Y):
    notX = set([notliteral(list(X)[0])])
    
    if notX.issubset(Y):
        return Y.difference(notX)
    else:
        return [X,Y]       

# Initial procedures to start resolution
def init_resolution(KB, alpha, StepByStep, SaveToFile):   
    # Compute Union
    Union = copy.deepcopy(KB)
    for literal in sentence[len(sentence)-1]:
        Union.append(set([notliteral(literal)]))
    
    while alpha:       
        # Apply Resolution Step by Step
        if StepByStep:
            result, output = ResolutionLoopSbS(Union)
            
            if SaveToFile: # save output to file
                outFileName = raw_input('\nInsert filename: ')        
                fo = open(outFileName+'.txt', "w")                
                #Write to file
                fo.write(output.getvalue())
                fo.close()                
            else: # print output to terminal
                print output.getvalue()
            output.close()
            
            if result == False:
                return 'False'   
            elif len(alpha) == 1:
                return 'True'
            else:
                alpha.pop()
        # Apply Resolution
        else:
            if ResolutionLoop(Union) == False:
                return 'False'   
            elif len(alpha) == 1:
                return 'True'
            else:
                alpha.pop()

# Convert list of sets to list of lists
def los2lol(SetFormat):
    ListFormat = []
    for item in SetFormat:
        ListFormat.append(list(item))
    return ListFormat
    
###############################
#          MAIN               #
###############################

# Read file from terminal
if len(sys.argv) == 2:
        filename = str(sys.argv[1])
else:
        print "\n\n ERROR: Please insert one correct filename\n\n"
        exit()

# Get list of sentences and print them
sentences = readfile(filename)

for i in range(len(sentences)):
    print i+1,')', fancyPrint(sentences[i])

# Select KB and sentence to prove
next = False
print 'Select Knowledge Base:'
while not next:
    userOption = raw_input('> ') 
    try:
        option = eval(userOption)-1  
    except:
        print 'Insert a valid option'
        option = -2
    if option != -2:
        if option not in range(len(sentences)):
            print 'Insert a valid option'
        else:
            KB = cnf(sentences[option])
            next = True

next = False
print 'Select sentence to prove:'
while not next:
    userOption = raw_input('> ') 
    try:
        option = eval(userOption)-1
    except:
        print 'Insert a valid option'
        option = -2
    if option != -2:
        if option not in range(len(sentences)):
            print 'Insert a valid option'
        else:
            sentence = cnf(sentences[option])
            next = True

# Main MENU
run = True

while(run):
    print '\n##############'
    print '#### MENU ####'
    print '##############\n'
    print '1. List Knowledge Base and Sentence to Prove'
    print '2. Prove using Resolution'
    print '3. Prove using Resolution (step by step)'
    print '4. Save to file'
    print '5. Save to file (using Resolution step by step)'
    print '6. Exit\n'
    userOption = raw_input('> ')   
    
    if userOption == '1':
        print 'KB: \t\t', los2lol(KB)
        print 'Sentence: \t', los2lol(sentence)
        raw_input('\nPress to continue...')
        
    elif userOption == '2':
        print init_resolution(KB, sentence, False, False)
        raw_input('\nPress to continue...')
        
    elif userOption == '3':
        print init_resolution(KB, sentence, True, False)
        raw_input('\nPress to continue...')    
            
    
    elif userOption == '4':
        outFileName = raw_input('\nInsert filename: ')        
        fo = open(outFileName+'.txt', "w")
        print init_resolution(sentence)
        
        #Write to file
        fo.write(init_resolution(sentence) + '\n')
        fo.close()
        raw_input('\nPress to continue...')

    elif userOption == '5':
        init_resolution(KB, sentence, True, True)
        raw_input('\nPress to continue...')

    elif userOption == '6':
        print 'Exiting!'
        run = False;
        
    else:
        print 'Invalid option\n'
        raw_input('\nPress to continue...')
