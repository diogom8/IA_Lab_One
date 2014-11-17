###############################
#       DEFINITIONS
###############################

filename = "input-example-2.txt"

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
    return sentence
    
def cnf(sentence):
    sentence = eliminate_implications(sentence)
    sentence = move_not_inwards(sentence)
    #print '.------------------------'
    sentence = distribute(sentence)
    
    return sentence

###############################
#          MAIN
###############################

sentences = readfile(filename)

for i in range(len(sentences)):
    print cnf(sentences[i])
    print '\n'
