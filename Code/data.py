execfile("bfs.py")

###SAVING DATA IN FILE FOR COMPARISON###
printed = False
fo = open("Output_Compare.txt", "r")
lines = fo.readlines()
fo.close()
fo = open("Output_Compare.txt", "w")
for line in lines:
    if line == ('@@ (U)'+filename+' @@\n'):
        fo.write(line)
        steps = 'Steps: '+str(len(name))
        nodes = ' Nodes: '+str(GeneratedNodes) 
        time  = ' time: '+str(ElapsedTime)+'seconds'
        fo.write( steps + nodes + time + '\n')
        lines.remove(line)
        printed = True
 
    else:
        fo.write(line)

if not printed:
    fo.write('@@ (U)'+filename+' @@\n')
    fo.write('Steps: '+str(len(name))+' Nodes: '+str(GeneratedNodes)+' time: '+str(ElapsedTime)+'seconds\n')
fo.close()
