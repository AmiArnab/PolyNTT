#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 09:13:45 2020

@author: arnab
"""

P = 536903681 # -1 = 1024 * 32 * 5 * 29 * 113

def Inv(x):
    
    p1bin = bin(P-2)
    p1bin = p1bin[::-1]
    
    y = FP(1)
    
    for i in p1bin:
        if(i=='1'):
            y = y * x
        x = x * x

    return y

def Exp(x,exp):
    
    p1bin = bin(exp)
    p1bin = p1bin[::-1]
    
    y = FP(1)
    
    for i in p1bin:
        if(i=='1'):
            y = y * x
        x = x * x

    return y

class FP:
    def __init__(self,tval=0):
        
        if tval < 0:
            self.x = P+tval
        else:
            self.x = tval if P > tval else (tval-P)
    def __add__(self,tval):
        t = FP(0)
        t.x = (self.x+tval.x)%P
        return t
    def __sub__(self,tval):
        t = FP(0)
        t.x = (self.x-tval.x)%P
        return t
    def __neg__(self):
        t = FP(0)
        t.x = P - self.x
        return t  
    def __mul__(self,tval):
        t = FP(0)
        t.x = (self.x*tval.x)%P
        return t
    def __invert__(self):
        t = Inv(self)
        return t
    def __pow__(self,exp):
        t = Exp(self,exp)
        return t
    def __repr__(self):
        return "FP"
    def __str__(self):
        return "("+str(self.x)+")"
    def __eq__(self,tval):
        if self.x == tval.x:
            return True
        else:
            return False
        
def FindGenerator2N():
    
    N = 100 #Till where to search
    f1 = FP(1)
    for v in range(2,N):
        g = FP(v)

        if g**(P-1) == f1:
            print "Got ",
            print g,    
            print "Subgroup orders ",
            for e in [2048,16,5,29,113]:
                print g**e,
                print ", ",
            print " "

def GenerateNthRootSet2N():
    g = FP(3) #group generator
    r = g**262160 #primitive root of unity or simply omega
    
    myomega = g**524320 #primitive root of unity or simply omega
    
    gp = [FP(0)] * 2048
    for v in range(0,2048):
        e = r**v
        gp[v] = e

    for v in gp:
        u = v**2048
        if not(u==FP(1)):
            print u,
            print "Fail!"
            
    for v in gp:
        u = v**2
        if u==myomega:
            print v,
            print "Wait! got one!!"
        
    return gp

def GenerateNthRootSet():
    g = FP(3) #group generator
    r = g**524320 #primitive root of unity or simply omega
    
    gp = [FP(0)] * 1024
    for v in range(0,1024):
        e = r**v
        gp[v] = e

#    for v in gp:
#        u = v**1024
#        if not(u==FP(1)):
#            print u,
#            print "Fail!"
        
    return gp

def CheckNRGroupGen():
    N = 100 #Till where to search
    for v in range(2,N):
        g = FP(v) #group generator
        g = g**524320 #primitive root of unity or simply omega
        print v,
        print "Order of g for each subgroup ",
        for e in [1024,32,5,29,113]:
            print g**e,
            print ", ",
        print " "

def GetPhiSet():
        
    g = FP(3) #group generator
    r = g**524320 #primitive root of unity or simply omega

    phi = FP(114984336)
#    phi2 = FP(421919345)

    gphi = [FP(0)] * 1024
    for v in range(0,1024):
        e = phi**v
        gphi[v] = e

    for v in gphi:
        u = v**2048
        if not(u==FP(1)):
            print u,
            print "Fail!"

    return gphi

def GetPhiSetN():

    phi = FP(114984336)
    phin = ~phi

    gphin = [FP(0)] * 1024
    for v in range(0,1024):
        e = phin**v
        gphin[v] = e
    return gphin
        
def ComputeOmegaN():
    omega = GenerateNthRootSet()
    omegan = [FP(0)]*len(omega)
    for i in range(len(omega)):
        v = omega[i]
        omegan[i] = ~v
    return omegan

def NTT(A):
    omega = GenerateNthRootSet()
    
    C = [FP(0)]*len(A)
    for i in range(0,len(A)):
        C[i] = FP(0)
        for j in range(0,len(A)):
            C[i] = C[i] + (A[j]*(omega[(i*j)%1024]))
            
    return C

def INTT(C):
    N = FP(1024)
    N1 = ~N
    
    omega = GenerateNthRootSet()
    omegan = [(~x)*N1 for x in omega]
    
    A = [FP(0)]*len(C)
    for i in range(0,len(C)):
        A[i] = FP(0)
        for j in range(0,len(C)):
            A[i] = A[i] + (C[j]*(omegan[(i*j)%1024]))
            
    return A

def PolyNTT(A,B):
    
    gphi = GetPhiSet()
    gphin = GetPhiSetN()
    
    A_bar = [(A[i] * gphi[i]) for i in range(0,len(A))]
    B_bar = [(B[i] * gphi[i]) for i in range(0,len(B))]

    AA = NTT(A_bar)
    BB = NTT(B_bar)
    
    CC = [(AA[i] * BB[i]) for i in range(0,len(AA))]
    
    C_bar = INTT(CC)
    C = [(C_bar[i] * gphin[i]) for i in range(0,len(C_bar))]
    
    return C

def PolyNTT_Test():
    A = [FP(0)] * 1024
    B = [FP(0)] * 1024
    
    A[1] = FP(5)
    A[2] = FP(10)
    A[3] = FP(20)
    
    B[1] = FP(2)
    B[2] = FP(3)
    B[3] = FP(5)
    
    C = PolyNTT(A,B)
    
    for c in C[:10]:
        print c
        
PolyNTT_Test()