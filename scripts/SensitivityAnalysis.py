# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 10:35:18 2016

@author: Ethan
"""

import DataBuilder as DB
import pywt
from sklearn import linear_model as lm

individualSize = 1000000
groupSize = 100
mutationOccurance = 1500
p = 1/mutationOccurance
numberOfMutations = 0
print("************")
for option in [1]:
    if(option == 1):
        numberOfMutations = 1
    elif(option == 2):
        numberOfMutations = 2
    elif(option == 3):
        numberOfMutations = 5
    elif(option == 4):
        numberOfMutations = 0
        #nothing needed here
    elif(option == 5):
        numberOfMutations = 2
    
    positionOfMutation = DB.mutationPositions(numberOfMutations,individualSize)
    percentOfGroup = .5
    ##############################################################
#        print("Starting to make group")
    group = DB.GroupBuilder(groupSize,DB.IndividualBuilder,[individualSize,[1],[p]])
    ##group = GroupBuilder(groupSize,SimplifiedIndividualBuilder,[individualSize,[1],[p]])
    groupZ, y, n = DB.MakeSick(group,positionOfMutation,percentOfGroup,option)
    noisePpl = []
    i = 0
    
    # write option 4 and 5's mutations positions for export
    if(option == 4):
        positionOfMutation = [[1000,3], n]
    elif(option == 5):
        positionOfMutation = [[[1000,3,'plus 2'], n], positionOfMutation]
    group = []
          
    ###############################################################
    yTrain = y[:90]
    yTest = y[90:]
    y = []
    normalizeRegressions = True
    models = [lm.ElasticNet]
    alphas = [.01]
    functions = ["haar"]
    levels = [4]
    for f in functions:
        trainingGroup = groupZ[:90]
        testingGroup = groupZ[90:]
        for l in levels:           
            for n in range(len(groupZ)):
                if (n < 90):
                    coeffs = pywt.wavedec(trainingGroup[n], f, level=l)
                    trainingGroup[n] = coeffs[0]
                else:
                    coeffs = pywt.wavedec(testingGroup[90-n], f, level=l)
                    testingGroup[90-n] = coeffs[0]
            #coeffs = []
            for m in models:
                for a in alphas:
                    clf = m(alpha = a,normalize = normalizeRegressions)
                    clf.fit(trainingGroup,yTrain)
                    
                    yPredicted = clf.predict(testingGroup)
                    yPredictedBin = yPredicted[:]
                    for i in range(len(yPredicted)):
                        yPredictedBin[i] = round(yPredicted[i])
                    DB.RunMeasures(yTest,yPredictedBin)[0]
#%%
pywt.waverec(coeffs,"haar")
a = list(clf.coef_)
maxA = max(a)
for i in range(a.count(maxA)):
    a.index(maxA)