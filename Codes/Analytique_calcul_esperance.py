import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt # !!!!!!! à importer
import tqdm as tq
import random
import math
from math import factorial
from mpmath import *
import decimal 
#import Decimal
from mpl_toolkits.mplot3d.axes3d import Axes3D
import queue as Q
def calculq(lamda,T,m2,p2,k):
    S=0
    for b2 in range(1,m2+1):    
      a=k*ln(lamda*T*b2)
      #a=(lamda*T*b2)**k
      b=ln(factorial(k))
      c=-lamda*T*b2
      d=ln(factorial(m2)/(factorial(b2)*factorial(m2-b2)))
      e=b2*ln(p2)+(m2-b2)*ln(1-p2)
      f=a-b
      S=S+exp(f+e+d+c)
    return S  
def sommeq(lamda,T,m2,p2,C):
    tab=[]
    C2=int(0.9*C)
    #lamda=alpha*C/(p2*m2*(1/d+1))
    for k in range(C2):
        tab.append(calculq(lamda,T,m2,p2,k))
    return sum(tab)     
def calculPi(lamda,T,m2,p2,k,B): 
   #for prec in range(1,nbre_pts):
        #d=0.05
        #alpha=0.5
        #lam_1=alpha*C/(p2*m2*(1/d+1))
        #print("lam1=",lam_1)
        #lam_2=alpha*C/(p2*m2*(d+1))
        #print("lam2=",lam_2)
        K=calculq(lamda,T,m2,p2,k)
        N=calculq(lamda,T,m2,p2,500)
        Pi=K*B/(1-N)
        return Pi  
def calculallPi(lamda,T,C,m2,p2,B):
    tab=[]
    tab_esp=[]
    C2=int(C)
    dicpi={}
    for k in range(C2):
        tab.append(calculPi(lamda,T,m2, p2, k, B))
        tab_esp.append(k*calculPi(lamda,T,m2, p2, k, B))
        A=sum(tab)
        B=sum(tab_esp)
        dicpi[k]=tab[k]
         #print("tab=",tab[k])
    f={'lamda_2':lamda,
       'nbre_etat':dicpi.keys(),
       'Pi':dicpi.values(),
       'Sum Pi':A}
    ff=pd.DataFrame(data=f)  
    with pd.ExcelWriter('dict_allPi_Cl2.xlsx', engine="openpyxl",mode='A') as writer:
       ff.to_excel(writer)
    return ff,B
def calculallPi2(T,C,m2,p2,B,N):
    list_lamda=[1.875,2.1875, 2.5, 2.8125, 3.125,3.4375,3.75,4.0625,4.375,4.6875,5,5.3125,5.625,5.9375,6.25,6.5625,6.875,7.1875,7.5,7.8125,8.125,8.4375,8.75,9.0625,9.375,9.6875,10,10.3125,10.625]
    print(len(list_lamda))
    list_esp=[]
    list_del=[]
    for i in range(N-1):
      tab=[]
      #C2=int(0.9*C)
      for k in range(C+1):
         tab.append(k*calculPi(list_lamda[i],T, m2, p2, k, B))
      A=sum(tab)
      list_esp.append(float(A))
      list_del.append(float(A/list_lamda[i]))
      len(list_esp)
         #print("tab=",tab[k])
    f={'lamda_2':list_lamda,
       'Espérance':list_esp,
       'Delay':list_del,}
    ff=pd.DataFrame(data=f)  
    with pd.ExcelWriter('Espérance_Cl2.xlsx', engine="openpyxl",mode='A') as writer:
      ff.to_excel(writer)
    return ff
def calculEA(m2,p2):
    S=0
    for b2 in range(1,m2+1):
      #print(b2) 
      #a=(lamda*T)**(k/b2)
      #g=floor(k/b2)
      #b=factorial(g)
      #if b==0 :
      #    b=1
      #c=np.exp(-lamda*T)
      d=factorial(m2)/(factorial(b2)*factorial(m2-b2))
      e=p2**b2*(1-p2)**(m2-b2)
      S=S+d*e
    return S 
def calculdEA(lamda,T,m2,p2):
    S=0
    for b2 in range(1,m2+1):
      a=lamda*T*b2
      #g=floor(k/b2)
      #b=factorial(g)
      #if b==0 :
      #    b=1
      #c=np.exp(-lamda*T)
      d=factorial(m2)/(factorial(b2)*factorial(m2-b2))
      e=p2**b2*(1-p2)**(m2-b2)
      S=S+a*d*e
    return S   
def calculEY(T,C,lamda,m2,p2,B):
    C2=int(0.9*C)
    A1=calculEA(m2, p2)
    B1=calculdEA(lamda, T, m2, p2)
    #C1=calculallPi(T, C, m2, p2, B)
    P1 = ((A1 * C2 - B1) / (A1 - 1) ** 2) * calculallPi(lamda, T, C, m2, p2, B)
    P2 = (A1 / (A1 - 1)) * calculallPi2(lamda, T, C, m2, p2, B)
    return P1 + P2
