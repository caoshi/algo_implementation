import numpy
import math
from sys import argv
#test_m1 = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
#m1 = [[11,2,3,4],[6,77,8,9],[11,12,13,14],[16,17,18,19]]
#test_m1 = numpy.matrix(test_m1)

#test_m2= [[1,2,3,4,5],[0,0,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
#m2 = [[1,2,3,4],[6,7,8,9],[11,12,13,14],[16,17,18,19]]
#test_m2 = numpy.matrix(test_m2)
#print m
#dim = 5
#print "log(dim)",math.log(dim,2),math.log(dim,2)/2
#print m[0:4,0:3]
def readMatrix():
    i = -1;
    fileb = open(argv[2],'r').readlines()
    fileb = fileb[1:]
    ib = 0
    #print fileb
    for line in open(argv[1],'r').readlines():
    #for line in open("a.txt",'r').readlines():
        if(i==-1):
            n = int(line.strip());
            matrix = numpy.zeros((n, n));
            matrixb = numpy.zeros((n, n)); 
        elif(i < n):

            tokens = line.strip().split(" ");
            x = i;
            for j in range(len(tokens)):
                v = float(tokens[j]);
                matrix[i][j] = v
            
        i=i+1;
    for line in fileb:
        tokensb = line.strip().split(" ")
        for jb in range(len(tokensb)):
            vb = float(tokensb[jb]);
            matrixb[ib][jb] = vb
        ib += 1
            
    return matrix,matrixb,n

    #return matrix,n
#print readMatrix()
test_m1,test_m2, dim = readMatrix()

    
def pad_out_zeros(Matrix, n):
    #Matrix,n readData()
    if (math.log(n,2)%2.0 == 0.0 ) :
        d = n
    else:
        n = int(math.log(n,2))+1
        d = pow(2,n)
    m = numpy.zeros(shape=(d,d))
    m[:dim,:dim] = Matrix
    m = numpy.matrix(m)
    #print m
    return m,d

test_m1,d = pad_out_zeros(test_m1, dim)
test_m2,d = pad_out_zeros(test_m2, dim)


def strassen(input_m1,input_m2,start,stop):
    """input 2 matrices and get the product by strassen's algo"""
    #print start, stop,"mid"
    if abs(start-stop)+1 == 2:#base case we have 2*2 matrix
        #print input_m1,input_m2
        #In this "if" clause input_m1 and input_m2 are two 2*2 matrix
        a00 = input_m1[0,0]
        a01 = input_m1[0,1]
        a10 = input_m1[1,0]
        a11 = input_m1[1,1]

        b00 = input_m2[0,0]
        b01 = input_m2[0,1]
        b10 = input_m2[1,0]
        b11 = input_m2[1,1]

        m1 = (a00+a11)*(b00+b11)
        m2 = (a10+a11)*b00
        m3 = a00*(b01-b11)
        m4 = a11*(b10-b00)
        m5 = (a00+a01)*b11
        m6 = (a10-a00)*(b00+b01)
        m7 = (a01-a11)*(b10+b11)

        c00 = m1+m4-m5+m7
        c01 = m3+m5
        c10 = m2+m4
        c11 = m1+m3-m2+m6
        
        return numpy.matrix([[c00,c01],[c10,c11]])

    mid = start+(stop-start)/2
    #print "x",mid
    
    A00 = input_m1[start:mid+1,start:mid+1]
    A10 = input_m1[mid+1:stop+1,start:mid+1]
    A01 = input_m1[start:mid+1,mid+1:stop+1]
    A11 = input_m1[mid+1:stop+1,mid+1:stop+1]

    B00 = input_m2[start:mid+1,start:mid+1]
    B10 = input_m2[mid+1:stop+1,start:mid+1]
    B01 = input_m2[start:mid+1,mid+1:stop+1]
    B11 = input_m2[mid+1:stop+1,mid+1:stop+1]
    #print A11,B11
    #return strassen(A10,B10,0,mid)

    A0011 = A00+A11
    B0011 = B00+B11
    A1011 = A10+A11
    B01_11= B01-B11
    B10_00 = B10-B00
    A0001 = A00+A01
    A10_00 = A10-A00
    B0001 = B00+B01
    A01_11 = A01-A11
    B1011=  B10+B11
    
    M1 = strassen(A0011,B0011,0,mid)
    M2 = strassen(A1011,B00,0,mid)
    M3 = strassen(A00,B01_11,0,mid)
    M4 = strassen(A11,B10_00,0,mid)
    M5 = strassen(A0001,B11,0,mid)
    M6 = strassen(A10_00,B0001,0,mid)
    M7 = strassen(A01_11,B1011,0,mid)
    
    C00 = M1+M4-M5+M7
    C01 = M3+M5
    C10 = M2+M4
    C11 = M1+M3-M2+M6

    C_upper = numpy.hstack((C00,C01))
    C_lower = numpy.hstack((C10,C11))
    C = numpy.vstack((C_upper,C_lower))
    
    return C[0:dim,0:dim]

    
print strassen(test_m1,test_m2,0,d-1)
#print m1,m2
#print "standard",test_m1.dot(test_m2)
