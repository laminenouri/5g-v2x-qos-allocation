import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt # !!!!!!! à importer
import tqdm as tq
import random
import simpy
import sys
import math
from collections import Counter
from scipy.stats import expon
from scipy.stats import poisson
""" code avec ajout de la fonction bino"""
def bino(m1,p1):
 A=np.random.binomial(m1, p1, 1)
 #print(A)
 while A==0:
   #print("A est nulle",A)
   A=np.random.binomial(m1, p1, 1)
   #print("nouvelle valeur",A)
 return A
def testing():
 A=np.random.random()
 a=2/5
 while A>=a:
     A=np.random.random()
 return A
def function_cl1(dic):
    dic_out={}
    A=list(dic.keys())
    D=list(dic.values())
    B=[]
    C=[]
    F=[]
    E=[]
    G=[]
    for i in range(len(A)):
       B.append(A[i][0]) 
       C.append(A[i][1])
    B1 = list(set(B))
    for j in range(len(B1)):
        pos1 = np.where(np.array(B) == B1[j])[0]
        F.append(pos1)
    for j in range(len(B1)):
        for k in list(F[j]):
          E.append(D[k])
        S=sum(E)
        E=[]
        G.append(S)
        dic_out[B1[j]]=G[j]
    return dic_out
def function_cl2(dic):
    dic_out={}
    A=list(dic.keys())
    D=list(dic.values())
    #B=[]
    C=[]
    F=[]
    E=[]
    G=[]
    for i in range(len(A)):
       C.append(A[i][1])
    C1 = list(set(C))
    for j in range(len(C1)):
        pos1 = np.where(np.array(C) == C1[j])[0]
        F.append(pos1)
    print(F)
    for j in range(len(C1)):
        for k in list(F[j]):
          E.append(D[k])
        S=sum(E)
        E=[]
        G.append(S)
        dic_out[C1[j]]=G[j]
    return dic_out
def calcul_attente(y):
    A=0
    if 450-y<0:
       A=y-450
    return A
def cal_esperance(index,proba):
    B=2000
    moy=np.array([0,0])
    for i in range(B):
        X_etoile=random.choices(index,proba)
        moy=np.array(X_etoile)+moy
    return (moy/B)[0]
def put(item,nbr,Y):
    return Y+[item]*nbr #rajoute nbr fois l'élèment item
def get(nbr,Y,temps):
    #print(Y[0:nbr])
    #print(temps)
    tmps=-np.sum(np.array(Y[0:nbr]))+nbr*temps
    #print(tmps)
    assert(tmps>=0)
    return Y[nbr:],tmps
"""une bande de 10 MHz (180khz), alors 50 RB peuvent être exploitées  espacement de 15khz donc 12bandes*15kHz=180 kHz 
1slot (1ms et 14 symboles) un RB est un slot de 12 bandes en 5G un RB (1 slot) transporte 14 symboles *12 bandes = 168 symboles en 1 ms 
Nombre de bits par symbole: Si MCS<=10 => Nbps = 2; Si MCS>=11 et MCS<=20=> Nbps = 4; Si MCS>=21 et  MCS<=28 =>  Nbps = 6;
un RB contient 84 symbole donc pour Nbps=2 on a 168*2=336bits
Pour classe 2 (classe prioritaire), on a m2=200 octets=1600 bits et p2= 0.3
Pour classe 1, on a m1=500 octets= 4000 bits et p1=0.6
Calcul du nombre de RBs (slots) maximum par message:
 Classe 2: 1600/336= 4,76 => 5RBs 
Classe 1: 4000/336= 11,9 => 12RBs
m2=5 (en RBs) et p2= 0.3 (plus de petits paquets) et m1=12 (en RBs) et p1= 0.6 (plus de grands paquets)
"""
def simulate_temps_poisson(N,lam_1,lam_2,m1,m2,p1,p2,C,pr1,pr2):
    C1=int(C*pr1)
    C2=int(C*pr2)
    C0=C-C1-C2
    assert (m1*p1*lam_1+m2*p2*lam_2<C),"condition de stabilité non vérifiée" #!!!!!!
    #Y_init=random.choices(index,proba)
    Aa1=[]
    Aa2=[]
    Temps11=[]
    Temps12=[]
    A1=poisson.rvs(lam_1) 
    print(A1)#tirage aléatoire de l'entrée A1
    A2=poisson.rvs(lam_2) #tirage aléatoire de l'entrée A1
    for i in range(A1):
        Aa1.append(bino(m1,p1))
    for j in range(A2):
        Aa2.append(bino(m2,p2)) 
    Temps11=[0]*A1
    Temps12=[0]*A2
    """for k in range(A1):
        Temps11.append(random.random())
    for l in range(A2):
        Temps12.append(random.random())"""
   # result1(lam_1,prec,m2,p2,N)
   # result2(lam_2,prec,m2,p2,N)
    #Aa1,Temps11=readfile1(prec,-1 , 0) #tirage aléatoire de l'entrée A1
    #Aa2,Temps12=readfile2(prec,-1 , 0) #tirag
    Y1=sorted(liste_temps(Temps11,Aa1))
    Y2=sorted(liste_temps(Temps12,Aa2))
    #Y1=Temps11
    #Y2=Temps12
    L_temps_1=[]
    L_temps_2=[]
    #Y1=put(0,Y_init[0][0],Y1)
    #Y2=put(0,Y_init[0][1],Y2)
    pop_1=0
    pop_2=0
    y1=len(Y1)
    y2=len(Y2)
    dic={}
    dic_del_2={}
    dic_att_2={}
    dic_del_par_RB_2={}
    dic_del_1={}
    dic_att_1={}
    dic_del_par_RB_1={}
    for n in tq.tqdm(range(1,N)): 
        dic[(y1,y2)]=dic.get((y1,y2),0)+1
        assert (pop_1>=0), 'dépassement'
        assert (pop_2>=0), 'dépassement'
        #Mariem: appel à la fonction bino pour ne pas avoir 0 comme résultat
        A1=[]
        A2=[]
        Temps1=[]
        Temps2=[]
        A11=poisson.rvs(lam_1) #tirage aléatoire de l'entrée A1
        A21=poisson.rvs(lam_2) #tirage aléatoire de l'entrée A1
        for i in range(A11):
           A1.append(bino(m1,p1))
        for j in range(A21):
           A2.append(bino(m2,p2)) 
        for k in range(A11):
           Temps1.append(n-1+random.random())
        for l in range(A21):
           Temps2.append(n-1+random.random())
        #return Temps1,Temps2
   # result1(lam_1,prec,m2,p2,N)
   # result2(lam_2,prec,m2,p2,N)
    #Aa1,Temps11=readfile1(prec,-1 , 0) #tirage aléatoire de l'entrée A1
    #Aa2,Temps12=readfile2(prec,-1 , 0) #tirag
        Arrivees1=sorted(liste_temps(Temps1,A1))
        Arrivees2=sorted(liste_temps(Temps2,A2))
        #return Arrivees1,Arrivees2
        #a1=bino(m1,p1)
        #a2=bino(m2,p2)
        #A1,Temps1=readfile1(prec,n-1 , n) #tirage aléatoire de l'entrée A1
        #A2,Temps2=readfile2(prec,n-1 , n) #tirage aléatoire de l'entrée A1
        #Arrivees1=liste_temps(Temps1,A1)
        #Arrivees2=liste_temps(Temps2,A2)
        etat_Y2=len(Y2)
        #print("etat_Y2", etat_Y2)
        etat_Y1=len(Y1)
        #assert(etat_Y2>C2)
        if etat_Y2<=C2:
            pop_2+=etat_Y2
            Y2,tps=get(etat_Y2,Y2,n)
            dic_del_2[(y1,y2,n)]=tps
            dic_att_2[(y1,y2,n)]=calcul_attente(y2)
            dic_del_par_RB_2[(y1,y2,n)]=round(tps/y2,2)
            L_temps_2.append(tps)
            if etat_Y1<=C0+C1: 
                pop_1+=etat_Y1
                Y1,tps=get(etat_Y1,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
            else:
                pop_1+=C0+C1
                Y1,tps=get(C0+C1,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
        elif etat_Y2<=C2+C0: #système saturé
            pop_2+=etat_Y2
            Y2,tps=get(etat_Y2,Y2,n)
            dic_del_2[(y1,y2,n)]=tps
            dic_att_2[(y1,y2,n)]=calcul_attente(y2)
            dic_del_par_RB_2[(y1,y2,n)]=round(tps/y2,2)
            L_temps_2.append(tps)
            if etat_Y1<=C1:
                pop_1+=etat_Y1
                Y1,tps=get(etat_Y1,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
            elif etat_Y1<= C-etat_Y2:
                pop_1+=etat_Y1
                Y1,tps=get(etat_Y1,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
            else:
                pop_1+=C-etat_Y2
                Y1,tps=get(C-etat_Y2,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
        elif etat_Y2>C2+C0 :
            pop_2+=C0+C2
            Y2,tps=get(C0+C2,Y2,n)
            dic_del_2[(y1,y2,n)]=tps
            dic_att_2[(y1,y2,n)]=calcul_attente(y2)
            dic_del_par_RB_2[(y1,y2,n)]=round(tps/y2,2)
            L_temps_2.append(tps)
            if etat_Y1<=C1:
                pop_1+=etat_Y1
                Y1,tps=get(etat_Y1,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
            else:
                pop_1+=C1
                Y1,tps=get(C1,Y1,n)
                L_temps_1.append(tps)
                dic_del_1[(y1,y2,n)]=tps
                dic_att_1[(y1,y2,n)]=calcul_attente(y1)
                dic_del_par_RB_1[(y1,y2,n)]=round(tps/y1,2)
        Y1=Y1+Arrivees1
        y1=len(Y1)
        #print(Y1)
        #Y2=put(n,A2,Y2)
        Y2=Y2+Arrivees2
        y2=len(Y2)
    dic_frequency2=dic
    for v in dic_frequency2.keys():
        dic_frequency2[v]=dic_frequency2[v]/N
   # print(dic_frequency)
    #functionplot(dic_frequency2) 
    return L_temps_1, L_temps_2,pop_1,pop_2,dic,dic_frequency2,dic_del_2,dic_att_2,dic_del_par_RB_2,dic_del_1,dic_att_1,dic_del_par_RB_1
def liste_temps(T,A1):
    L=[]
    for i in range(len(T)):
        for j in range(int(A1[i])):
            L.append(T[i])
    return L
def courbe_temps_attente_dom(N,nbre_pts=30,pas=0.01,alpha=0.5):
    '''1=m1*p1*lamda_1+m2*p2*lamda_2/C,alpha=m1*p1*lam_1+m2*p2*lam_2/C'''
    list_stab=[]
    list_tmps_att1_pois=[]
    list_tmps_att2_pois=[]
    list_esp1_pois=[]
    list_esp2_pois=[]
    list_lamda1=[]
    list_lamda2=[]
    list_dom=[]
    list_esperance_Cl1_anal=[]
    list_esperance_Cl2_anal=[]
    #list_A1=[]
    #list_A2=[]
    T=0.01
    m1=48
    m2=20
    p1=0.6
    p2=0.4
    C=500
    pr1=0.05 #Mariem : 10% de ressources garanties pour la classe 1
    pr2=0
    C1=int(C*pr1)
    C2=int(C*pr2)
    C0=C-C1-C2
    for prec in range(1,nbre_pts):
        d=pas
        lam_1=(1-(0.05+d))*alpha*C/(p1*m1)
        #lam_1=alpha*C/(p1*m1*(d+1))
        print("lam1=",lam_1)
        #lam_2=alpha*C/(p2*m2*(1/d+1))
        lam_2=(0.05+d)*alpha*C/(p2*m2)
        print("lam2=",lam_2)
        ##poisson
        #print(dic_frequency)
        #Mariem :index, proba pour calculer Y_init
        L_temps_1, L_temps_2, pop_1, pop_2, dic, dic_frequency2,dic_del_2,dic_att_2,dic_del_par_RB_2,dic_del_1,dic_att_1,dic_del_par_RB_1=simulate_temps_poisson(N,lam_1,lam_2,m1,m2,p1,p2,C,pr1,pr2)
        // ...existing code...
        dcprob = pd.DataFrame(data=cprob)  
        with pd.ExcelWriter('dict_compose_poisson_Cl2_proba%d.xlsx'% (prec), engine="openpyxl", mode='w+') as writer:
           dcprob.to_excel(writer)
        cprob1={'lamda_1':lam_1,
           'lamda_2':lam_2,
           'dic_nbre_clients_poisson_1_keys': dic_out_poisson_1.keys(),
           'dic_nbre_clients_prob_poisson_1_values': dic_out_poisson_1.values(),}
           //'temps_attente_classe_2':L_temps_2}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcprob1 = pd.DataFrame(data=cprob1)  
        with pd.ExcelWriter('dict_compose_poisson_Cl1_proba%d.xlsx'% (prec), engine="openpyxl", mode='w+') as writer:
           dcprob1.to_excel(writer)
        // ...existing code...
        #Mariem : ind,prob pour calculer l'éspérance
        #for m in dic_del_2.keys():
        for d in dic_del_2.keys():
            dic_del_2[d]=np.rint(dic_del_2[d])
        Del_freq_poisson=dict(Counter(dic_del_par_RB_2.values()))
        for e in Del_freq_poisson.keys():
            Del_freq_poisson[e]=Del_freq_poisson[e]/N
        Del_Cl1_freq_poisson=dict(Counter(dic_del_par_RB_1.values()))
        for e in Del_Cl1_freq_poisson.keys():
            Del_Cl1_freq_poisson[e]=Del_Cl1_freq_poisson[e]/N
            //e=np.rint(e)
        //return L1
        dic_out_poisson_1=function_cl1(dic_frequency2)
        dic_out_poisson_2=function_cl2(dic_frequency2)
        ind,prob=np.array(list(dic.keys())),((1/N)*np.array(list(dic.values()))) //formatage(M)
        esp=cal_esperance(ind,prob)
        list_esp1_pois.append(esp[0])
        list_esp2_pois.append(esp[1])
        tmps_att_1,tmps_att_2=np.sum(np.array(L_temps_1)/pop_1),np.sum(np.array(L_temps_2)/pop_2)
        list_tmps_att1_pois.append(tmps_att_1)
        list_tmps_att2_pois.append(tmps_att_2)
        list_stab.append(alpha)
        list_lamda1.append(lam_1)
        list_lamda2.append(lam_2)
        list_dom.append(m1*p1*lam_1/(m2*p2*lam_2))
        list_esperance_Cl1_anal.append(m1*p1*T*lam_1)
        list_esperance_Cl2_anal.append(m2*p2*T*lam_2)
        //poisson
        cfreq={'lamda_1':lam_1,
           'lamda_2':lam_2,
           'dic_frequency_poisson_2_keys': dic_frequency2.keys(),
           'dic_frequency_poisson_2_values': dic_frequency2.values(),}
           //'temps_attente_classe_2':L_temps_2}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcfreq = pd.DataFrame(data=cfreq) 
        with pd.ExcelWriter('dict_compose_poisson_freq%d.xlsx'% (prec), engine="openpyxl",mode='w') as writer:
           dcfreq.to_excel(writer,sheet_name='dict_compose_poisson_freq')  
        cprob={'lamda_1':lam_1,
           'lamda_2':lam_2,
           'dic_nbre_clients_poisson_2_keys': dic_out_poisson_2.keys(),
           'dic_nbre_clients_prob_poisson_2_values': dic_out_poisson_2.values(),}
           //'temps_attente_classe_2':L_temps_2}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcprob = pd.DataFrame(data=cprob)  
        with pd.ExcelWriter('dict_compose_poisson_Cl2_proba%d.xlsx'% (prec), engine="openpyxl", mode='w+') as writer:
           dcprob.to_excel(writer)
        cprob1={'lamda_1':lam_1,
           'lamda_2':lam_2,
           'dic_nbre_clients_poisson_1_keys': dic_out_poisson_1.keys(),
           'dic_nbre_clients_prob_poisson_1_values': dic_out_poisson_1.values(),}
           //'temps_attente_classe_2':L_temps_2}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcprob1 = pd.DataFrame(data=cprob1)  
        with pd.ExcelWriter('dict_compose_poisson_Cl1_proba%d.xlsx'% (prec), engine="openpyxl", mode='w+') as writer:
           dcprob1.to_excel(writer)
        cprob1={'lamda_1':lam_1,
           'lamda_2':lam_2,
           'dic_nbre_clients_poisson_1_keys': dic_out_poisson_1.keys(),
           'dic_nbre_clients_prob_poisson_1_values': dic_out_poisson_1.values(),}
           //'temps_attente_classe_2':L_temps_2}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcprob1 = pd.DataFrame(data=cprob1)  
        with pd.ExcelWriter('dict_compose_poisson_Cl1_proba%d.xlsx'% (prec), engine="openpyxl", mode='A') as writer:
           dcprob1.to_excel(writer)
        cdel={'lamda_1':lam_1,
              'lamda_2':lam_2,
              //'dic_frequency_keys': dic_frequency2.keys(),
              //'dic_frequency_values': dic_frequency2.values(),
              'nbre_clients_système_poisson':dic_del_2.keys(),
              'delai_classe_2_poisson':dic_del_2.values(),
              'attente_classe2_poisson':dic_att_2.values(),
              'dic_del_par_RB_2_poisson':dic_del_par_RB_2.values(),}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcdel = pd.DataFrame(data=cdel)  
        with pd.ExcelWriter('dict_compose_poisson_Cl2_del%d.xlsx'% (prec), engine="openpyxl",mode='A') as writer:
           dcdel.to_excel(writer)
        cdelf={'lamda_1':lam_1,
              'lamda_2':lam_2,
              //'dic_frequency_keys': dic_frequency2.keys(),
              //'dic_frequency_values': dic_frequency2.values(),
              'delai_classe_2_poisson':Del_freq_poisson.keys(),
              'freq_delai_classe2_poisson':Del_freq_poisson.values(),}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcdelf = pd.DataFrame(data=cdelf)  
        with pd.ExcelWriter('dict_compose_poisson_Cl2_del_freq%d.xlsx'% (prec), engine="openpyxl",mode='A') as writer:
           dcdelf.to_excel(writer)    
        cdelclass1={'lamda_1':lam_1,
              'lamda_2':lam_2,
              //'dic_frequency_keys': dic_frequency2.keys(),
              //'dic_frequency_values': dic_frequency2.values(),
              'nbre_clients_système_poisson':dic_del_2.keys(),
              'delai_classe_1_poisson':dic_del_1.values(),
              'attente_classe1_poisson':dic_att_1.values(),
              'dic_del_par_RB_1_poisson':dic_del_par_RB_1.values(),}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcdelcl1 = pd.DataFrame(data=cdelclass1)  
        with pd.ExcelWriter('dict_compose_poisson_Cl1_del%d.xlsx'% (prec), engine="openpyxl",mode='A') as writer:
           dcdelcl1.to_excel(writer)
        cdelfclass1={'lamda_1':lam_1,
              'lamda_2':lam_2,
              //'dic_frequency_keys': dic_frequency2.keys(),
              //'dic_frequency_values': dic_frequency2.values(),
              'delai_classe_1_poisson':Del_Cl1_freq_poisson.keys(),
              'freq_delai_classe_1_poisson':Del_Cl1_freq_poisson.values(),}
          // 'dic_frequency_poisson_1_keys': dic_out_poisson_1.keys(),
          // 'dic_frequency_poisson_1_values': dic_out_poisson_1.values(),
        dcdelf = pd.DataFrame(data=cdelfclass1)  
        with pd.ExcelWriter('dict_compose_poisson_Cl1_del_freq%d.xlsx'% (prec), engine="openpyxl",mode='A') as writer:
           dcdelf.to_excel(writer)  

    d = {'rapport_stabilité': list_stab, 
         'tmps-att1-pois': list_tmps_att1_pois, 
         'tmps-att2-pois':list_tmps_att2_pois,
         'lamda_1':list_lamda1,
         'lamda_2':list_lamda2,
         'rapport_dom':list_dom,
         'esperance-Y1-pois':list_esp1_pois,
         'esperance-Y2-pois':list_esp2_pois,
         'esperance_Cl1_anal':list_esperance_Cl1_anal,
         'esperance_Cl2_anal':list_esperance_Cl2_anal,
         'm1':[m1]*(nbre_pts-1),
         'm2':[m2]*(nbre_pts-1),
        'p1':[p1]*(nbre_pts-1),
        'p2':[p2]*(nbre_pts-1),