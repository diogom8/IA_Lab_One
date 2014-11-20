###############################
#       DEFINITIONS
###############################
from sets import Set

import sys
if len(sys.argv) == 2:
        filename = str(sys.argv[1])
else:
        print "\n\n ERROR: Please insert only one correct filename\n\n"
        exit()


###############################
#       FUNCTIONS
###############################

# reads a list of tuples from file
def readfile(filename):
    with open(filename) as f:
        sentences = []
        for line in f:
            sentences.append(eval(line))
    return sentences

# checks if s is atomic
def isAtomic(s):
    if isinstance(s, basestring) or (s[0] == 'not' and isinstance(s[1], basestring)):
        return True
    return False

# replaces a <=> b with [a or not(b)] and [b or not(a)]
# and replaces a => b with [not(a) or b]
def eliminate_implications(sentence):
    if not isAtomic(sentence):
        if sentence[0] == 'not': # just check first operand
            if not isAtomic(sentence[1]):
                new1 = eliminate_implications(sentence[1])
                sentence = (sentence[0], new1)        
        else:
            # check if first operand is atomic
            if not isAtomic(sentence[1]):
                new1 = eliminate_implications(sentence[1])
                sentence = (sentence[0], new1, sentence[2])
            # check if second operand is atomic
            if not isAtomic(sentence[2]):
                new2 = eliminate_implications(sentence[2])
                sentence = (sentence[0], sentence[1], new2)
            # in case both operands are atomic, check operator            
            a = sentence[1]
            b = sentence[2]            
            if sentence[0] == '<=>':
                return ('and', ('or',a,('not',b)), ('or',b,('not',a)))
            elif sentence[0] == '=>':
                return ('or', ('not',a), b)
    return sentence

# moves not inwards in order to just have nots in literals
def move_not_inwards(sentence):
    if not isAtomic(sentence):
        if sentence[0] == 'not': # just check first operand
            if not isAtomic(sentence[1]):
                new1 = move_not_inwards(sentence[1])
                sentence = (sentence[0], new1)
            # check if sentence[1] is negation of literal
            lowerOp = sentence[1][0]
            if lowerOp == 'not':
                sentence = sentence[1][1] # not not A = A 
            elif lowerOp == 'and':
                # not(a and b) = [not(a) or not(b)]
                sentence = ('or',('not',sentence[1][1]),('not',sentence[1][2]))
            elif lowerOp == 'or':
                # not(a or b) = [not(a) and not(b)]
                sentence = ('and',('not',sentence[1][1]),('not',sentence[1][2]))          
        else:
            # check if first operand is atomic
            if not isAtomic(sentence[1]):
                new1 = move_not_inwards(sentence[1])
                sentence = (sentence[0], new1, sentence[2])
            # check if second operand is atomic
            if not isAtomic(sentence[2]):
                new2 = move_not_inwards(sentence[2])
                sentence = (sentence[0], sentence[1], new2)

    return sentence

# applies distributivity law distributing 'or's over 'and's wherever possible 
def distribute(sentence):
    if not isAtomic(sentence):
        if sentence[0] == 'not': # just check first operand
            if not isAtomic(sentence[1]):
                new1 = distribute(sentence[1])
                sentence = (sentence[0], new1)
        else:
            # check if first operand is atomic
            if not isAtomic(sentence[1]):
                new1 = distribute(sentence[1])
                sentence = (sentence[0], new1, sentence[2])
            # check if second operand is atomic
            if not isAtomic(sentence[2]):
                new2 = distribute(sentence[2])
                sentence = (sentence[0], sentence[1], new2)
            
            if not isAtomic(sentence[1]) and sentence[0] == 'or':
                if sentence[1][0] == 'and':
                    a = sentence[1][1]
                    b = sentence[1][2]
                    c = sentence[2]
                    return distribute(('and',('or',c,a),('or',c,b)))                                    
            elif not isAtomic(sentence[2]) and sentence[0] == 'or':
                if sentence[2][0] == 'and':
                    a = sentence[2][1]
                    b = sentence[2][2]
                    c = sentence[1]
                    return distribute(('and',('or',c,a),('or',c,b)))     
    return sentence
printMap = {'not':'~','or':'\\/','and':'/\\','<=>':'<=>','=>':'=>'}
# printing in user-friendly way
def fancyPrint(s):
    if s == ():
        return '()'
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
    
def simplify(sentence,userOption):
    opli_sent = [sentence]
    opli_clause = []
    clauses = []
    NliteralsBefore = 0
    i = 0
    while len(opli_sent) != 0:
        if opli_sent[0][0] == 'and':
            opli_sent.extend([opli_sent[0][1],opli_sent[0][2]])
            
        elif isAtomic(opli_sent[0]):
            clauses.append(set([]))
            clauses[i].add(opli_sent[0])
            i+=1
            NliteralsBefore += 1
            #convert to set_ i++
        else:
            clauses.append(set([]))
            opli_clause.extend([opli_sent[0][1],opli_sent[0][2]])
            while len(opli_clause) != 0:
                if isAtomic(opli_clause[0]):
                    clauses[i].add(opli_clause[0])
                    NliteralsBefore += 1
                else:
                    opli_clause.extend([opli_clause[0][1],opli_clause[0][2]])
                
                opli_clause.pop(0)
            i+=1


        opli_sent.pop(0)
        NliteralsAfter = 0
        for x in clauses:
            NliteralsAfter += len(x)
        
    #Simplification 1: Remove repeated literals in clauses (performed when sets are defined)
    if userOption == '2' and NliteralsBefore != NliteralsAfter:
        print '\n\nStep: Remove repeated literals in clauses\n'
        print fancyPrint(outputFormat(clauses))
    
    
    #Simplification 2: Remove subsets
    indexToRemove = []
    for i in range(len(clauses)-1):
        for j in range(i+1,len(clauses)):
            if clauses[i].issubset(clauses[j]):
                if i not in indexToRemove:
                    indexToRemove.append(i)
                
            elif clauses[i].issuperset(clauses[j]):
                if j not in indexToRemove:
                    indexToRemove.append(j)
    for i in range(len(indexToRemove)):
        clauses.pop(indexToRemove[i]-i) 
    
    if userOption == '2' and len(indexToRemove) != 0:
        print '\n\nStep: Remove subsets\n'
        print fancyPrint(outputFormat(clauses))
    
                
    #Simplification 3: Remove inverse clauses
    solo_clauses = []
    for x in clauses:
        if len(x) == 1:
            if notliteral(list(x)[0]) in solo_clauses:
                clauses = []
                break;
            else:
                solo_clauses.append(list(x)[0])
    
    if userOption == '2' and clauses == []:
        print '\n\nStep: Clean impossible sentences in case of inverse clauses\n'
        print fancyPrint(outputFormat(clauses))
            
    
    return outputFormat(clauses)

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
        outputSentence = ()
        
    if len(outputClause) > 1:
        outputSentence = ('and',outputClause[0],outputClause[1])
        for j in range(2,len(outputClause)):
            outputSentence = ('and',outputSentence,outputClause[i])
    elif len(outputClause) == 1:
        outputSentence = outputClause[0]
        
    return outputSentence
    
       
def cnf(sentence,userOption):
    prev_sentence = sentence
    if userOption == '2':
        sentence = eliminate_implications(sentence)
        if prev_sentence != sentence:        
            print '\n\nStep: Eliminate Implications\n'
            print fancyPrint(sentence)
        prev_sentence = sentence

        sentence = move_not_inwards(sentence)
        if prev_sentence != sentence:        
            print '\n\nStep: Move negation inwards\n'
            print fancyPrint(sentence)
        prev_sentence = sentence
                
        sentence = distribute(sentence)
        if prev_sentence != sentence:        
            print '\n\nStep: Distributivity Law\n'
            print fancyPrint(sentence)
        prev_sentence = sentence        
        

        sentence = simplify(sentence,userOption)
    else:
        sentence = eliminate_implications(sentence)
        sentence = move_not_inwards(sentence)
        sentence = distribute(sentence)
        sentence = simplify(sentence,userOption)
    return sentence

###############################
#          MAIN               #
###############################

sentences = readfile(filename)
CNFsentences = []
run = True


print '------ CNF Converter ------\n\n'
print 'Filename:'+filename+'\n\n'

while(run):
    print '\n\n          ## MENU ##\n'
    print '1. List all sentences before conversion\n'
    print '2. Step-by-step conversion\n'
    print '3. List all sentences after conversion\n'
    print '4. Save to file\n'
    print '5. Exit\n'
    userOption = raw_input('> ')
    
    
    if userOption == '1':
        for i in range(len(sentences)):
            print 'Clause '+str(i)+': '+fancyPrint(sentences[i])
        raw_input('\nPress to continue...') 
        
    elif userOption == '2':
        for i in range(len(sentences)):
            print 'Clause '+str(i)+': '+fancyPrint(sentences[i])
        try: 
            sentenceOption = int(raw_input('Pick option> '))
            if sentenceOption < len(sentences):
                cnf(sentences[sentenceOption],'2')
            else:
                print '\n Not a valid option! Returning to menu.'
            raw_input('\nPress to continue...')   
        except ValueError:
            print '\n Not a valid option! Returning to menu.'
        

    elif userOption == '3':
        for i in range(len(sentences)):
            CNFsentences.append(cnf(sentences[i],'3'))
            print 'Clause '+str(i)+': '+fancyPrint(CNFsentences[i])
        raw_input('\nPress to continue...')    
            
    
    elif userOption == '4':
        outFileName = raw_input('\nInsert filename: ')        
        fo = open(outFileName+'.txt', "w")
        
        if CNFsentences == []:
            for i in range(len(sentences)):
                CNFsentences.append(cnf(sentences[i],'3'))
        
        for sentence in CNFsentences:
            fo.write(str(sentence)+'\n')
        fo.close()
        raw_input('\nPress to continue...')
    elif userOption == '5':
        print 'Exiting!'
        run = False;
        
    else:
        print 'Only single-digit numbers (1-5) are allowed\n'
        
    
    
