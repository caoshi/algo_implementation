from collections import deque
from sys import argv

def readData():
    """save edge cost between node as dictionary{(u,v):w},
       save adjacency list as list of list [[2],[1,3],...] meaning node 0 is connected with node 2,   
    """
    graphDict ={}
    with open(argv[1], 'r') as f:
        firstLine = f.readline()
        Num = firstLine.split()[0]
        #next(f)
        vertexList = [[]]*int(Num)# vertex [[2],[1,3,4]] means vertex 0 has connection with 2
                                  # vertex 1 has connection with 1,3,4, so initialize it first
        for line in f:
            #print line
            lineList = line.split()
            if int(lineList[0])> int(lineList[1]):
                print "make sure the edges are sorted in nondecreasing order"
            graphDict[(int(lineList[0]),int(lineList[1]))]=float(lineList[2])
            #print int(lineList[0])

            if vertexList[int(lineList[0])] == []:
                vertexList[int(lineList[0])] = [int(lineList[1])]
            else:
                vertexList[int(lineList[0])].append(int(lineList[1]))
            #seems some redundancy check happended
            #But this can handle some missing input such as input 0 1 2, 2 3,then edge 1 to 0 is missing
            #in the raw input, but the program can get the [[1,2],[0],[0,3]] right form as well.   
            if vertexList[int(lineList[1])] == []:
                vertexList[int(lineList[1])] = [int(lineList[0])]
            else:
                vertexList[int(lineList[1])].append(int(lineList[0]))
    return graphDict,vertexList, int(Num)

#print readData()
graphDict, vertexList, Num = readData()

def DFS(startNode = 0):
    """input a Graph G(V,E), and travers every vetex by DSF"""
    S = [] #use list as stack
    #startNode = 0
    S.append(startNode)
    visiting = [0]*Num
    Output = []
    while len(S) != 0:
        #x = S[-1]
        x = S.pop()
        if x not in Output:
            Output.append(x)
        if visiting[x] == 0:
            visiting[x] =1
            for v in vertexList[x][::-1]:#[::-1] gives the visiting order from small node to larger one
                if visiting[v] == 0:
                    S.append(v)
    return Output

def BFS(startNode = 0):
    """input a Graph G(V,E), and travers every vetex by DSF"""
    Squeue = deque([]) #use list as quene
    #startNode = 0
    Squeue.append(startNode)
    visiting = [0]*Num
    Output = []
    while len(Squeue) != 0:
        #x = S[-1]
        x = Squeue.popleft()
        if x not in Output:
            Output.append(x)
        if visiting[x] == 0:
            visiting[x] =1
            for v in vertexList[x]:
                if visiting[v] == 0:
                    Squeue.append(v)
    return Output

def Prim(startNode=0):
    #graphDict, vertex, Num= readData()
    MST = [] #put edge cost instead edge name in this homework.
    visit = [startNode] #set the first one
    minEdgeDict = {}
    length = len(visit)
    #print length, Num
    outputWeight = 0
    while length != Num:
        #print length, Num
        minEdge = 65535
        for i in range(length):#visit[i] is a vertex, i.e. 1, 2, ...and saving based on zero index
            if vertexList[visit[i]] != []: #means the vertex is connecting to some others
                for v in vertexList[visit[i]]:
                    if v in visit:
                        continue
                    else:
                        # we only save (v,u) as key where v <u for space saving so edgeCost shoud be looked in the right order
                        if visit[i] > v: 
                            edgeCost = graphDict[(v,visit[i])] 
                        if visit[i] < v:
                            edgeCost = graphDict[(visit[i],v)]
                        if edgeCost <= minEdge:
                            minEdge = edgeCost
                            vMin = v
                            #Just for formating as homework required
                            if visit[i]<v:
                                tempV = v
                                tempU = visit[i]
                            else:
                                tempV = visit[i]
                                tempU = v
                            minEdgeDict[(tempU,tempV)]=minEdge
        MST.append(minEdge)
        outputWeight += minEdge
        visit.append(vMin)
        length = len(visit)
        #print vMin
        #print "length", length
    #print visit
    return minEdgeDict, outputWeight

def Floyd():
    D = [[65535]*Num for n in range(Num)] #use list of list as Matrix to avoid import numpy
                          # set 65535 as infinity
    S = [[Num+1]*Num for n in range(Num)]  #successor matrix
    
    for i in range(Num):
        for j in range(Num):
            S[i][j] = j
            S[j][i] = i
            if (i,j) in graphDict:
                D[i][j] = graphDict[(i,j)]
                D[j][i] = graphDict[(i,j)]
            if j == i:
                D[i][j] = 0
    #print D,"D1"
    #print S,"S1"
    for k in range(Num):
        for i in range(Num):
            for j in range(Num):
                if D[i][j]>D[i][k]+D[k][j]:
                    D[i][j] = D[i][k]+D[k][j]
                    S[i][j] = S[i][k]
                #tempDij = D[i][j]
                #D[i][j] = min(D[i][j],(D[i][k]+D[k][j]))
                #if D[i][j] != tempDij:
                    #S[i][j] = S[i][k]
    #D,S are ready to use, The codes below is for tracking path and output
    shortestPair = []
    pathTotal = []
    for i in range(Num):
        for j in range(i+1,Num):
            pathi = []
            pathi.append(i)
            x = i
            while (x != j):
                x = S[x][j]
                pathi.append(x)
            #pathi.sort()
            pathOutput = str(pathi[0])+"->"+str(pathi[-1])
            pathTotal.append(pathi)
    #return pathTotal
            
    #below just for homework outputformating
    OutputPath = []
    OutputWeight = []
    
    for path in pathTotal:
        Output1 = []
        length = len(path)
        weight = 0
        for i in range(length-1):
            edgeL = [path[i],path[i+1]]
            edgeL.sort()
            weight += graphDict[(edgeL[0],edgeL[1])]
            Output1.append((edgeL[0],edgeL[1],graphDict[(edgeL[0],edgeL[1])]))
        OutputPath.append(Output1)
        OutputWeight.append(weight)
    return OutputPath,OutputWeight
            
#print Floyd()

if __name__ == "__main__":
    
    print "Depth First Search Traversal:"
    print  DFS(0) #start at node 0, if you want, you can change to anyother nodes.
    print
    print "Breadth First Search Traversal:"
    print  BFS(0)
    print 
    print "Minimum Spanning Tree:"
    E, W = Prim(0)
    #codes below are just for output as required by homework
    print  "V = " , [i for i in range(Num)]
    OutputFormatE = []
    for key, value in sorted(E.iteritems(), key=lambda (k,v): (v,k)):
        OutputFormatE.append((key[0],key[1],value))
    print  "E = ", [e for e in OutputFormatE]
    print "Total Weight:", W
    print
    print "Shortest Paths:"
    OutputPath,OutputWeight = Floyd()
    counter = 0
    for i in range(Num):
        for j in range(i+1,Num):
            print i,"->",j, "=", OutputPath[counter]
            print "  Path Weight = ", OutputWeight[counter]
            counter +=1
##            
        
    
        
