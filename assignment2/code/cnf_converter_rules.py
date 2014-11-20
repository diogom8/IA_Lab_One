###############################
#       CNF Converter Rules   #
###############################
from sets import Set
from cnf_converter_auxiliary import *
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
                return move_not_inwards(sentence)
            elif lowerOp == 'and':
                # not(a and b) = [not(a) or not(b)]
                sentence = ('or',('not',sentence[1][1]),('not',sentence[1][2]))
                return move_not_inwards(sentence)
            elif lowerOp == 'or':
                # not(a or b) = [not(a) and not(b)]
                sentence = ('and',('not',sentence[1][1]),('not',sentence[1][2])) 
                return move_not_inwards(sentence)         
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

def simplify(sentence,userOption):
    fifo_sentence = [sentence]
    fifo_clause = []
    clauses = []
    NliteralsBefore = 0
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
        NliteralsAfter = 0
        for x in clauses:
            NliteralsAfter += len(x)
        
    #Simplification 1: Remove repeated literals in clauses (performed when sets are defined)
    if userOption == '2' and NliteralsBefore != NliteralsAfter:
        print '\n\nStep: Remove repeated literals in clauses\n'
        print fancyPrint(outputFormat(clauses))
    


    #Simplification 2: Erase clauses with inverse literals and set sentece to true if it is single-clause
    clauseToRemove = []
    Bf_clauses = len(clauses)
    for clause in clauses:
        for i in range(len(clause) - 1):
            for j in range(i+1,len(clause)):
                if list(clause)[i] == notliteral((list(clause)[j])):
                      clauseToRemove.append(clause)
                      break   
            if clause in clauseToRemove:
                break

    for clause in clauseToRemove:
        clauses.remove(clause)
    
    if clauses == [] and Bf_clauses != 0:
        clauses = [set(['true'])]
        
    if userOption == '2' and len(clauseToRemove) != 0:
        print '\n\nStep: Erase clauses with inverse literals\n'
        print fancyPrint(outputFormat(clauses))
    
    

    #Simplification 3: Remove supersets or equal sets between clauses
    indexToRemove = []
    for i in range(len(clauses)-1):
        for j in range(i+1,len(clauses)):
            if clauses[i].issubset(clauses[j]):
                if j not in indexToRemove:
                    indexToRemove.append(j)
                
            elif clauses[i].issuperset(clauses[j]):
                if i not in indexToRemove:
                    indexToRemove.append(i)
    for i in range(len(indexToRemove)):
        clauses.pop(indexToRemove[i]-i) 
    
    if userOption == '2' and len(indexToRemove) != 0:
        print '\n\nStep: Remove supersets or equal sets within clauses\n'
        print fancyPrint(outputFormat(clauses))
    
                
    #Simplification 4: Remove inverse clauses
    solo_clauses = []
    for x in clauses:
        if len(x) == 1:
            if notliteral(list(x)[0]) in solo_clauses:
                clauses = [set(['false'])]
                break;
            else:
                solo_clauses.append(list(x)[0])
    
   
    if userOption == '2' and clauses == [set(['false'])]:
        print '\n\nStep: Clean impossible sentences in case of inverse clauses\n'
        print fancyPrint(outputFormat(clauses))
            
    
    
    return outputFormat(clauses)
