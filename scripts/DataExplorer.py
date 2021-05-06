# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 21:02:05 2016

@author: Ethan
"""

import matplotlib.pyplot as plt
import csv

def ReadGroupFromFile(fileName):
    """ read a group from a csv file"""
    with open(fileName, 'r') as f:  #opens file
        group = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists
    for i in range(len(group)):
        group[i] = [int(x) for x in group[i]]
    return group

numClassMethods = 4
numRow = 7 #window sizes
numColmn = 9 #datasets
#
#fig, ax = plt.subplot(numRow,numColmn)

fileName = 'D:\\Users\\Ethan\\Documents\\Google Drive\\Project\\Compiled Report.csv'

with open(fileName, 'r') as f:  #opens file
    group = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists
headers = group[0]
group = group[1:]
m = 1
for l in range(4): #algorithms
    for k in range(7): #windows
        print(group[0][4] + group[4][3])
        for j in range(9):  #groups
            alpha = []
            roc = []
            
            for i in range(12):
                alpha.append(float(group[i][5]))
                roc.append(float(group[i][6]))
            #plt.scatter(alpha,roc)
            if((m-1)%9 == 0):
                ax = plt.subplot(numRow,numColmn,m)                
                plt.ylabel('ROC')
            else:
                plt.subplot(numRow,numColmn,m,sharey = ax)
                plt.ylabel('ROC')
            
            plt.semilogx(alpha,roc,'.')
            plt.axis([1e-16,1e2,-0.1,1.1])
            if (m < 10):
                plt.title(group[0][2])
            
            if(m>=54):
                plt.xlabel('alpha')
            group = group[12:]
            m = m +1
    plt.show()
    m=1