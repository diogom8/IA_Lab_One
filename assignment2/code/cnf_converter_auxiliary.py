###################################
#       CNF Converter Auxiliary   #
###################################
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
        literal = ('not',literal[0])
    return literal    
#Return sentence in intended output format. Input: list of clauses in set format       
def outputFormat(clauses):
    outputClause = []
    if len(clauses) >= 1:
        for i in range(len(clauses)):
            outputClause.append(())
            literals = list(clauses[i])
            if len(literals) > 1:
                outputClause[i] = ('or',literals[0],literals[1])
                for j in range(2,len(literals)):
                    outputClause[i] = ('or',literals[j],outputClause[i])
            elif len(literals) == 1:           
                outputClause[i] = literals[0]
    else:
        return '(empty)'
        
    if len(outputClause) > 1:
        outputSentence = ('and',outputClause[0],outputClause[1])
        for j in range(2,len(outputClause)):
            outputSentence = ('and',outputSentence,outputClause[i])
    elif len(outputClause) == 1:
        outputSentence = outputClause[0]
        
    return outputSentence
