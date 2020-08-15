#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 08:51:44 2020

@author: arnab
"""

#P = 2941249 # -1 = 64 * 3 * 15319
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

def FindGenerator():
    
    N = 100 #Check for first few generators (here all are generators till 100)
    f1 = FP(1)
    for v in range(2,N):
        g = FP(v)
        if g**(P-1) == f1:
            print "Got ",
            print g,    
            print "Subgroup orders ",
            for e in [1024,32,5,29,113]:
                print g**e,
                print ", ",
            print " "
            
def GenerateGroup():
    
    g = FP(5)
    gp = set()
    for v in range(1,P):
        e = g**v
        gp.add(e.x)

def GenerateNthRootSet():
    g = FP(3) #group generator
    r = g**524320 #primitive root of unity or simply omega
    
    gp = [FP(0)] * 1024
    for v in range(0,1024):
        e = r**v
        gp[v] = e
        
    for v in gp:
        u = v**1024
        if not(u==FP(1)):
            print u,
            print "Fail!"
        
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

def ComputeOmegaN():
    omega = GenerateNthRootSet()
    omegan = [(~x)*N1 for x in omega]
    return omegan

def NTT(A):
    omega = GenerateNthRootSet() #These will be stored in memory in hardware
    
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
    omegan = [(~x)*N1 for x in omega] #These will be stored in memory in hardware
    
    A = [FP(0)]*len(C)
    for i in range(0,len(C)):
        A[i] = FP(0)
        for j in range(0,len(C)):
            A[i] = A[i] + (C[j]*(omegan[(i*j)%1024]))
            
    return A


#FindGenerator()
#CheckNRGroupGen()
#GenerateGroup()
#GenerateNthRootSet()
#ComputeOmegaN()

    
A = [FP(0)] * 1024

A[1] = FP(5)
A[2] = FP(10)
A[3] = FP(20)

C = NTT(A)
E = INTT(C)

for e in E[:10]:
    print e