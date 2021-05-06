# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 16:37:39 2016

@author: Ethan
"""

import DataBuilder as DB
import random
import pywt
from sklearn import linear_model as lm
from datetime import datetime

#individualSize = 1000000
#groupSize = 100
#mutationOccurance = 1500
#p = 1/mutationOccurance
#noisePercent = 0
#option = 4
#for noisePercent in [0, .01, .025, .5]:
#    print("****************************************************")
#    for option in [1,1,2,2,3,3,4,4,5,5]:
#        print("****************************************************")
#        if(option == 1):
#            numberOfMutations = 1
#        elif(option == 2):
#            numberOfMutations = 2
#        elif(option == 3):
#            numberOfMutations = 5
#        elif(option == 4):
#            numberOfMutations = 0
#            #nothing needed here
#        elif(option == 5):
#            numberOfMutations = 2
#        positionOfMutation = DB.mutationPositions(numberOfMutations,individualSize)
#        percentOfGroup = .5
#        gTest = DB.GroupBuilder(groupSize,DB.IndividualBuilder,[individualSize,[1],[p]])
#        gSick, y, n = DB.MakeSick(gTest,positionOfMutation,percentOfGroup,option)
#        #introduce noise        
#        noiseNumber = 0        
#        for i in range(len(gSick)):
#                if(random.random() < noisePercent):
#                    y[i] = abs(y[i]-1)
#                    noiseNumber = noiseNumber + 1
#        if(option == 4):
#            positionOfMutation = [[1000,3], n]
#        elif(option == 5):
#            positionOfMutation = [[[1000,3,'plus 2'], n], positionOfMutation]
#       
#        populatedCols = []
#        newGroup = []
#        for i in range(individualSize):
#            colSum = 0
#            for j in range(groupSize):
#                colSum = colSum + gSick[j][i]
#                if(colSum > 0):
#                    populatedCols.append(i);
#                    if(len(newGroup) == 0):
#                        for k in range(groupSize):
#                            newGroup.append([gSick[k][i]])
#                    else:
#                        for k in range(groupSize):
#                            newGroup[k].append(gSick[k][i])
#                    break
#        
#        yTrain = y[:90]
#        yTest = y[90:]
#        a = .01
#        m = lm.ElasticNet
#        f = "haar"
#        levels = [0,5,6,7]
#        normalizeRegressions = True
#        
#        for l in levels:
#            trainingGroup = newGroup[:90]
#            testingGroup = newGroup[90:]
#            compiledCoeffs = []         
#            for n in range(len(gSick)):
#                if (n < 90):
#                    coeffs = pywt.wavedec(trainingGroup[n], f, level=l)
#                    trainingGroup[n] = coeffs[0]       
#                else:
#                    coeffs = pywt.wavedec(testingGroup[90-n], f, level=l)
#                    testingGroup[90-n] = coeffs[0]
#                compiledCoeffs.append(coeffs)
#            clf = m(alpha = a,normalize = normalizeRegressions)
#            clf.fit(trainingGroup,yTrain)
#            
#            yPredicted = clf.predict(testingGroup)
#            yPredictedBin = yPredicted[:]
#            for i in range(len(yPredicted)):
#                yPredictedBin[i] = round(yPredicted[i])
#            measure = DB.RunMeasures(yTest,yPredictedBin)
#            
#            #nonzero = []
#            #c = clf.coef_
#            
#            #for i in range(len(c)):
#            #    if(c[i] != 0):
#            #        nonzero.append([i,c[i]])
#            #        if(c[i] == max(c)):
#            #            print(i)
#            #            print(c[i])
#            if(measure == [1.0]):
#                print("##^## NOISE#:",str(noiseNumber),"OPTION:",option,"LEVEL:",str([l,len(trainingGroup[0])]),"MEASURE:",str(measure),"##^##")
#            else:
#                print("NOISE#:",str(noiseNumber),"OPTION:",option,"LEVEL:",str([l,len(trainingGroup[0])]),"MEASURE:",str(measure))
#              
#            #maxV = max(c)        
##
##%%

individualSize = 1000000
groupSize = 100
mutationOccurance = 1500
p = 1/mutationOccurance
#noisePercent = 0.1 # this is the percentage chance than an individual is noise, NOT the percentage of the group that will be noise
#option = 1
numberOfMutations = 0
header = ["Dataset", "Noise %", "Option", "Position of Mutation","Compression Method",
          "Level/Window Size","Individual Size","model","alpha","ROC AUC"]
#results = []
#results.append(header)
compMethod = ""
for noisePercent in [.05]:
    print("************")
    for option in [1,1,1,1,1,
                   2,2,2,2,2,
                   3,3,3,3,3,
                   4,4,4,4,4,
                   5,5,5,5,5]:
        print(str(noisePercent),".",str(option))
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
        windowSizes = [1,1500]
        compMethod  = "None"
        ##############################################################
#        print("Starting to make group")
        group = DB.GroupBuilder(groupSize,DB.IndividualBuilder,[individualSize,[1],[p]])
        ##group = GroupBuilder(groupSize,SimplifiedIndividualBuilder,[individualSize,[1],[p]])
        groupZ, y, n = DB.MakeSick(group,positionOfMutation,percentOfGroup,option)
        noisePpl = []
        i = 0
        # Insert noise
        while(len(noisePpl) < (noisePercent*groupSize)):
            try:
                noisePpl.index(i%100)
            except:           
                if(random.random() < noisePercent):
                    y[i%100] = abs(y[i%100]-1)
                    noisePpl.append(i%100)
            i = i + 1
        noisePpl.sort()
        
        # write option 4 and 5's mutations positions for export
        if(option == 4):
            positionOfMutation = [[1000,3], n]
        elif(option == 5):
            positionOfMutation = [[[1000,3,'plus 2'], n], positionOfMutation]
        group = []
        
        ##
        if(noisePercent == 0):
            fileName = "Group_" + str(option) + "_" + str(datetime.now()).replace("-","").replace(" ","_").replace(":","")[:-7]+".csv"
        else:
            fileName = "Group_Noised" + str(int(noisePercent*100)) + "_" + str(option) + "_" + str(datetime.now()).replace("-","").replace(" ","_").replace(":","")[:-7]+".csv"
        yfileName = "yFor_" + fileName
        fileLocation = "D:\\Users\\Ethan\\Documents\\Google Drive\\Project\\Data Files\\"
        
        fullFile = fileLocation + fileName
        yfullFile = fileLocation + yfileName
#        print("Starting to write csv")
        DB.WriteGroupToFile(groupZ,fullFile)
        DB.WriteGroupToFile(y,yfullFile)
#        print("csv written")        
        ###############################################################
        yTrain = y[:90]
        yTest = y[90:]
        y = []
        normalizeRegressions = True
        #models = [lm.ElasticNet, lm.Lasso, lm.LassoLars]
        models = [lm.ElasticNet]
        alphas = [.01]
        for w in windowSizes:
            if(w==1):
                windowedGroupZ = groupZ
                compMethod = "None"
            else:
                windowedGroupZ = DB.WindowizeGroup(groupZ,w)
                compMethod = "Windowed"
            trainingGroup = windowedGroupZ[:90]
            testingGroup = windowedGroupZ[90:]
            windowedGroupZ = []
        ### analysis #####################################################
            for m in models:
                for a in alphas:
                    clf = m(alpha = a,normalize = normalizeRegressions)
                    clf.fit(trainingGroup,yTrain)
        
                    yPredicted = clf.predict(testingGroup)
                    yPredictedBin = yPredicted[:]
                    for i in range(len(yPredicted)):
                        yPredictedBin[i] = round(yPredicted[i])
                    
                    #Dataset, Sick ppl for Dataset, Window Size, model,alpha,...
                    report = [[fullFile, yfullFile],noisePercent, option, 
                              positionOfMutation,compMethod,w,
                              len(trainingGroup[0]), "ElasticNet", str(a),
                              DB.RunMeasures(yTest,yPredictedBin)[0]]
                    results.append(report)
        ### analysis #####################################################
    #    functions = ["haar",
    #                 "db1",
    #                 "sym8",
    #                 "sym14",
    #                 "sym18",
    #                 "rbio5.5",
    #                 "rbio3.9",
    #                 "rbio2.8",
    #                 "rbio1.5",
    #                 "rbio1.3",
    #                 "rbio1.1",
    #                 "bior1.5",
    #                 "bior1.1"]
    #    functions = ["haar","db1","bior1.1","rbio1.1"]
        
        functions = ["haar"]
        levels = [1, 2, 3, 4, 5, 6, 7]
        for f in functions:
            compMethod = "Wavelet: " + f
            trainingGroup = groupZ[:90]
            testingGroup = groupZ[90:]
            for l in levels:           
                for n in range(len(groupZ)):
                    if (n < 90):
                        coeffs = pywt.wavedec(trainingGroup[n], f, level=1)
                        trainingGroup[n] = coeffs[0]
                    else:
                        coeffs = pywt.wavedec(testingGroup[90-n], f, level=1)
                        testingGroup[90-n] = coeffs[0]
                coeffs = []
                for m in models:
                    for a in alphas:
                        clf = m(alpha = a,normalize = normalizeRegressions)
                        clf.fit(trainingGroup,yTrain)
                        
                        yPredicted = clf.predict(testingGroup)
                        yPredictedBin = yPredicted[:]
                        for i in range(len(yPredicted)):
                            yPredictedBin[i] = round(yPredicted[i])
                        
                        #Dataset, Sick ppl for Dataset, Window Size, model,alpha,...
                        report = [[fullFile, yfullFile],noisePercent, option, 
                              positionOfMutation,compMethod,l,
                              len(trainingGroup[0]), "ElasticNet", str(a),
                              DB.RunMeasures(yTest,yPredictedBin)[0]]
                        results.append(report)                    
        
        newGroup = []
        for i in range(individualSize):
            colSum = 0
            for j in range(groupSize):
                colSum = colSum + groupZ[j][i]
                if(colSum > 0):
                    if(len(newGroup) == 0):
                        for k in range(groupSize):
                            newGroup.append([groupZ[k][i]])
                    else:
                        for k in range(groupSize):
                            newGroup[k].append(groupZ[k][i])
                    break
        
        models = [lm.ElasticNet]
        alphas = [.01]
        for w in [1,100]:
            if(w==1):
                windowedGroupZ = newGroup
                compMethod = "Zero Reduction - None"
            else:
                windowedGroupZ = DB.WindowizeGroup(newGroup,w)
                compMethod = "Zero Reduction - Windowed"
            trainingGroup = windowedGroupZ[:90]
            testingGroup = windowedGroupZ[90:]
            windowedGroupZ = []
        ### analysis #####################################################
            for m in models:
                for a in alphas:
                    clf = m(alpha = a,normalize = normalizeRegressions)
                    clf.fit(trainingGroup,yTrain)
        
                    yPredicted = clf.predict(testingGroup)
                    yPredictedBin = yPredicted[:]
                    for i in range(len(yPredicted)):
                        yPredictedBin[i] = round(yPredicted[i])
                    
                    #Dataset, Sick ppl for Dataset, Window Size, model,alpha,...
                    report = [[fullFile, yfullFile],noisePercent, option, 
                              positionOfMutation,compMethod,w,
                              len(trainingGroup[0]), "ElasticNet", str(a),
                              DB.RunMeasures(yTest,yPredictedBin)[0]]
                    results.append(report)
        
        functions = ["haar"]
        levels = [1, 2, 3, 4, 5, 6, 7]
        for f in functions:
            compMethod = "Zero Reduction - Wavelet: " + f
            trainingGroup = newGroup[:90]
            testingGroup = newGroup[90:]
            for l in levels:            
                for n in range(len(newGroup)):
                    if (n < 90):
                        coeffs = pywt.wavedec(trainingGroup[n], f, level=1)
                        trainingGroup[n] = coeffs[0]
                    else:
                        coeffs = pywt.wavedec(testingGroup[90-n], f, level=1)
                        testingGroup[90-n] = coeffs[0]
                coeffs = []
                for m in models:
                    for a in alphas:
                        clf = m(alpha = a,normalize = normalizeRegressions)
                        clf.fit(trainingGroup,yTrain)
                        
                        yPredicted = clf.predict(testingGroup)
                        yPredictedBin = yPredicted[:]
                        for i in range(len(yPredicted)):
                            yPredictedBin[i] = round(yPredicted[i])
                        
                        #Dataset, Sick ppl for Dataset, Window Size, model,alpha,...
                        report = [[fullFile, yfullFile],noisePercent, option, 
                              positionOfMutation,compMethod,l,
                              len(trainingGroup[0]), "ElasticNet", str(a),
                              DB.RunMeasures(yTest,yPredictedBin)[0]]
                        results.append(report) 
reportFile = fileLocation + "reportlog_" + str(option)+ "_" + str(datetime.now()).replace("-","").replace(" ","_").replace(":","")[:-7] +".csv"
DB.WriteResultsToReport(results,reportFile)
        
