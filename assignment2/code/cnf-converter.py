from cnf_converter_rules import *
from cnf_converter_auxiliary import *
import sys

if len(sys.argv) == 2:
        filename = str(sys.argv[1])
else:
        print "\n\n ERROR: Please insert one correct filename\n\n"
        exit()

###############################
#       FUNCTIONS             #
###############################

# reads a list of tuples from file
def readfile(filename):
    try:
        with open(filename) as f:
            sentences = []
            for line in f:
                sentences.append(eval(line))
    except IOError:
        print 'ERROR: File "' + filename + '" does not exist!'
        quit()
    return sentences

# Conjunctive Normal Form Algorithm
def cnf(sentence,userOption):
    prev_sentence = sentence
    #Step-by step way
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

        #Conversion to list of disjunctions
        clausesList,NliteralsBefore = convert2list(sentence) 
        if prev_sentence != sentence:        
            print '\n\nStep: Distributivity Law\n'
            print fancyPrint(sentence)
            
               
        clausesList = simplify(clausesList,NliteralsBefore,userOption)

        print '\n\nFinal Output\n'
        print clausesList
    #No step-by-step way
    else:
        sentence = eliminate_implications(sentence)
        sentence = move_not_inwards(sentence)
        sentence = distribute(sentence)

        #Conversion to list of disjunctions
        clausesList,NliteralsBefore = convert2list(sentence) 
        clausesList = simplify(clausesList,NliteralsBefore,userOption)
    return clausesList

###############################
#          MAIN               #
###############################

sentences = readfile(filename)
CNFsentences = []
run = True

print '------ CNF Converter ------'
print 'Filename: '+filename+'\n\n'

while(run):
    print '\n          ## MENU ##\n'
    print '1. List all sentences before conversion\n'
    print '2. Step-by-step conversion\n'
    print '3. List all sentences after conversion\n'
    print '4. Save to file\n'
    print '5. Exit\n'
    userOption = raw_input('> ')   
    
    if userOption == '1':
        for i in range(len(sentences)):
            print 'Sentence '+str(i)+': '+fancyPrint(sentences[i])
        raw_input('\nPress to continue...') 
        
    elif userOption == '2':
        for i in range(len(sentences)):
            print 'Sentence '+str(i)+': '+fancyPrint(sentences[i])
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
            print 'Sentence '+str(i)+': '+str(CNFsentences[i])
        raw_input('\nPress to continue...')    
            
    
    elif userOption == '4':
        outFileName = raw_input('\nInsert filename: ')        
        fo = open(outFileName+'.txt', "w")
        #If simplification not performed yet
        if CNFsentences == []:
            for i in range(len(sentences)):
                CNFsentences.append(cnf(sentences[i],'3'))
        #Write to file
        for sentence in CNFsentences:
            fo.write(str(sentence)+'\n')
        fo.close()
        raw_input('\nPress to continue...')
    elif userOption == '5':
        print 'Exiting!'
        run = False;
        
    else:
        print 'Only single-digit numbers (1-5) are allowed\n'
    
