#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 13:45:32 2020

@author: arnab
"""

P = 47 #Filed prime
n = 23 #n point NTT, P = 1 mod 2n, also n should be power of 2 for implementation

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
    
    N = P
    f1 = FP(1)
    for v in range(2,N):
        g = FP(v)
        if g**(P-1) == f1:
            print "Got ",
            print g,
            print "Subgroup orders ",
            print g**23,
            print g**2
            
def GenerateGroup():
    
    g = FP(5)
    gp = set()
    for v in range(1,P):
        e = g**v
        gp.add(e.x)

def GenerateNthRootSet():
    g = FP(5) #group generator
    r = g**2 #primitive root of unity
    
    gp = [FP(0)] * 23
    for v in range(0,23):
        e = r**v
        gp[v] = e
        
#    print gp
#    
#    for v in gp:
#        print v**23 # if if it is really n-th root of unity
        
    return gp

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
            C[i] = C[i] + (A[j]*(omega[(i*j)%23]))
            
    return C

def INTT(C):
    N = FP(n)
    N1 = ~N
    
    omega = GenerateNthRootSet()
    omegan = [(~x)*N1 for x in omega]
    
    g = FP(25)
    g = ~g
    
    A = [FP(0)]*len(C)
    for i in range(0,len(C)):
        A[i] = FP(0)
        for j in range(0,len(C)):
            A[i] = A[i] + (C[j]*(omegan[(i*j)%23]))
            
    return A

#Polynomial Coefficients
A = [FP(1), FP(2), FP(0), FP(0), FP(0), FP(0), FP(0), FP(0), FP(1), FP(2), FP(5), FP(7), FP(8), FP(2), FP(4), FP(5), FP(7), FP(8), FP(2), FP(4), FP(6), FP(7), FP(2)]
C = NTT(A)

#NTT Coeffifients
for c in C:
    print c
print " "

E = INTT(C)

#Origianl Coefficients, same as A
for e in E:
    print e