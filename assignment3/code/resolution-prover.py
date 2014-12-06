from cnf_converter_rules import *
from cnf_converter_auxiliary import *
import sys
#if len(sys.argv) == 2:
#        filename = str(sys.argv[1])
#else:
#        print "\n\n ERROR: Please insert one correct filename\n\n"
#        exit()
filename = 'input-example.txt'

###############################
#       FUNCTIONS             #
###############################

# reads a list of tuples from file
def readfile(filename):
    KB = []            
    sentence = []
    try:
        f = open(filename)
        lines = f.readlines()
        #Read KB
        KB = (eval(lines[1]))
        #Read sentence to prove
        sentence = (eval(lines[3]))
    except IOError:
        print 'ERROR: File "' + filename + '" does not exist!'
        quit()
    return KB,sentence

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
                        UNION.remove(UNION[j])
                        UNION.append(result)
                        NewClauses = True
                        break
                    
            if NewClauses:
                break
                                    
                       
    return False

def countLiterals(UNION):
    SUM = 0
    for item in UNION:
        if len(item) == 1:
            SUM += 1
    return SUM
   
def resolution(X,Y):
    notX = set([notliteral(list(X)[0])])
    
    if notX.issubset(Y):
        return Y.difference(notX)
    else:
        return [X,Y]       
    
###############################
#          MAIN               #
###############################

#From Reading one may get a list of clauses for KB (KB) and
# a sentence to prove (sentence)
KB,sentence = readfile(filename)

#Convert sentence to prove to CNF format
sentence = cnf(sentence)
#From now on, sentence is a list of clauses
while sentence:
    UNION = list(KB)
    
    for literal in list(sentence[len(sentence)-1]):
        UNION.append(set([notliteral(literal)]))
    

    if ResolutionLoop(UNION) == False:
        print 'False'
        break    
    elif len(sentence) == 1:
        print 'True'
        break
    else:
        sentence.pop()
