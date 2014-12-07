#######################################
# CNF Converter Auxiliary Functions   #
#######################################

# checks if s is atomic
def isAtomic(s):
    if isinstance(s, basestring) or (s[0] == 'not' and isinstance(s[1], basestring)):
        return True
    return False

# printing in user-friendly way
def fancyPrint(s):
    printMap = {'not':'~','or':'\\/','and':'/\\','<=>':'<=>','=>':'=>'}
    if s == '(false)' or s == '(true)' or s == '(empty)':
        return s
    elif not isAtomic(s):
        if s[0] == 'not':
            return printMap['not']+fancyPrint(s[1])
        else:
            return '('+fancyPrint(s[1])+' '+printMap[s[0]]+' '+fancyPrint(s[2])+')'
            
    else:
        if s[0] == 'not':
            return printMap['not']+s[1]
        else:
            return s

#Return logical not of input literal    
def notliteral(literal):
    if literal[0] == 'not':
        literal = literal[1]
    else:
        literal = ('not', literal)
    return literal

#Converts sentence in input format to a list of clauses(defined as sets of literals)
def convert2list(sentence):

    fifo_sentence = [sentence]
    fifo_clause = []
    clauses = []
    NliteralsBefore = 0
    NliteralsAfter = 0
    i = 0
    while len(fifo_sentence) != 0:
        if fifo_sentence[0][0] == 'and':
            fifo_sentence.extend([fifo_sentence[0][1],fifo_sentence[0][2]])
            
        elif isAtomic(fifo_sentence[0]):
            clauses.append(set([]))
            clauses[i].add(fifo_sentence[0])
            i+=1
            NliteralsBefore += 1
        else:
            clauses.append(set([]))
            fifo_clause.extend([fifo_sentence[0][1],fifo_sentence[0][2]])
            while len(fifo_clause) != 0:
                if isAtomic(fifo_clause[0]):
                    clauses[i].add(fifo_clause[0])
                    NliteralsBefore += 1
                else:
                    fifo_clause.extend([fifo_clause[0][1],fifo_clause[0][2]])
                
                fifo_clause.pop(0)
            i+=1


        fifo_sentence.pop(0)

    return (clauses,NliteralsBefore)
        
     

