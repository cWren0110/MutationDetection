# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 18:27:58 2016

@author: Ethan Wade
"""
import random
import csv
from sklearn import metrics


def IndividualBuilder(size, possList, probList):
    """
    Args:
        size (int) - the list size to be created
        PossArr - a list of the possible mutations
            types (mutation, deletion,...)
        ProbArr - a list of the probibilities of the possible
            mutations occuring.
    Returns:
        individual (list)
    """
    if(len(list(possList)) != len(list(probList))):
        raise Exception('len(PossArr) != len(ProbArr)')
    individual = [0]*size
    random.seed()
    for i in range(size):
        for j in range(len(possList)):
            if(random.random() <= probList[j]):
                individual[i] = possList[j]
    return individual

def GroupBuilder(size, builderFunc, indAttr):
    """size - the number of members of the group
       indAttr - a list of [size, possList, probList] for IndividualBuilder
       file - the csv file to rebuild an existing group from"""
    individualSize = indAttr[0]
    possList = indAttr[1]
    probList = indAttr[2]
    group = []
    for i in range(size):
        group.append(builderFunc(individualSize,possList,probList))
    return group

def WriteGroupToFile(group,fileName):
    """ write group as a csv to file"""
    try:
        with open(fileName,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(group)
    except:
        print("Group only has one entry")
        with open(fileName,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(group)
    
def ReadGroupFromFile(fileName):
    """ read a group from a csv file"""
    with open(fileName, 'r') as f:  #opens file
        group = list(list(rec) for rec in csv.reader(f, delimiter=',')) #reads csv into a list of lists
    for i in range(len(group)):
        group[i] = [int(x) for x in group[i]]
    return group

def MakeSick(group, pos, p, option):
    """group of individuals,
    position that indicates sickness,
    p - percentage of group to be sick
    option indicates the 'option' of sickness applied"""
    returnGroup = group
    groupSize = len(returnGroup)
    numSick = round(groupSize*p)
    n = random.randint(0, len(group[0]) - 1001)
    if(option == 1):
        pos = pos[0]
        for i in range(groupSize):
            returnGroup[i][pos] = 0
            if(i < numSick):
                returnGroup[i][pos] = 1
        pos = [pos]
    elif(option == 2):
        random.seed()        
        for i in range(groupSize):
            returnGroup[i][pos[0]] = 0
            returnGroup[i][pos[1]] = 0
            if(i < numSick):
                if(random.random() < .5):
                    returnGroup[i][pos[0]] = 1
                else:
                    returnGroup[i][pos[1]] = 1
    elif(option == 3):
        random.seed()
        n = random.randint(2, 5)
        for i in range(groupSize):
            if(i < numSick):
                returnGroup[i][pos[0]] = 0
                returnGroup[i][pos[1]] = 0
                returnGroup[i][pos[2]] = 0
                returnGroup[i][pos[3]] = 0
                returnGroup[i][pos[4]] = 0
                while(returnGroup[i][pos[0]] + returnGroup[i][pos[1]] + returnGroup[i][pos[2]] + returnGroup[i][pos[3]] + returnGroup[i][pos[4]] < n):
                    r = random.random()
                    if(r < .2):
                        returnGroup[i][pos[0]] = 1
                    elif(r < .4):
                        returnGroup[i][pos[1]] = 1
                    elif(r < .6):
                        returnGroup[i][pos[2]] = 1
                    elif(r < .8):
                        returnGroup[i][pos[3]] = 1
                    else:
                        returnGroup[i][pos[4]] = 1
            else:
                # don't automatically zero out, just make sure there aren't
                # two or more mutations                
                while(returnGroup[i][pos[0]] + returnGroup[i][pos[1]] + returnGroup[i][pos[2]] + returnGroup[i][pos[3]] + returnGroup[i][pos[4]] > 1):
                    r = random.random()
                    if(r < .2):
                        returnGroup[i][pos[0]] = 0
                    elif(r < .4):
                        returnGroup[i][pos[1]] = 0
                    elif(r < .6):
                        returnGroup[i][pos[2]] = 0
                    elif(r < .8):
                        returnGroup[i][pos[3]] = 0
                    else:
                        returnGroup[i][pos[4]] = 0
    elif(option == 4):
        random.seed()
        m = n + 1001
        for i in range(groupSize):
            if(i < numSick):
                while(sum(returnGroup[i][n:m]) < 3):
                    r = n + random.randint(0,1000)
                    returnGroup[i][r] = 1
            else:
                for j in range(1000):
                    r = n + j                    
                    if(sum(returnGroup[i][n:m]) < 3):
                        break
                    if(returnGroup[i][r] == 1):
                        returnGroup[i][r] = 0
    elif(option == 5):
        random.seed()
        m = n + 1001
        for i in range(groupSize):
            if(i < numSick):
                returnGroup[i][pos[0]] = 1
                returnGroup[i][pos[1]] = 1
                while(sum(returnGroup[i][n:m]) < 3):
                    r = n + random.randint(0,1000)
                    returnGroup[i][r] = 1
            else:
                for j in range(1000):
                    r = n + j                    
                    if(sum(returnGroup[i][n:m]) < 3):
                        break
                    if(returnGroup[i][r] == 1):
                        returnGroup[i][r] = 0
    
    returnGroup = ShuffleGroup(returnGroup)
    return returnGroup, findY(returnGroup,pos,option,n), n

def findY(group,pos,option,n):
    """finds who is sick based upon option and pos"""
    groupSize = len(group)
    y = [0]*groupSize
    if(option == 1):
        pos = pos[0]
        for i in range(groupSize):
            if(group[i][pos] == 1):
                y[i] = 1
    elif(option == 2):
        for i in range(groupSize):
            if(group[i][pos[0]] == 1 or group[i][pos[1]] == 1):
                y[i] = 1
    elif(option == 3):
        for i in range(groupSize):
            if(group[i][pos[0]] + group[i][pos[1]] + group[i][pos[2]] + group[i][pos[3]] + group[i][pos[4]] > 1):
                y[i] = 1
    elif(option == 4):
        m = n + 1001        
        for i in range(groupSize):
            if(sum(group[i][n:m]) >= 3):
                y[i] = 1
    elif(option == 5):
        m = n + 1001        
        for i in range(groupSize):
            if((sum(group[i][n:m]) >= 3) and (group[i][pos[0]] == 1 and group[i][pos[1]] == 1)):
                y[i] = 1
    return y
                   
def ShuffleGroup(group):
    """resorts a group randomly"""
    Y = []
    random.seed()
    for i in range(len(group)):
        Y.append(random.random())
    sortedGroup = [x for (y,x) in sorted(zip(Y,group), key=lambda pair: pair[0])]   
    return sortedGroup

def Windowize(windowSize, individual):
    """Reduce individual size by summing the number of mutations
       in a window and replacing all values with that sum."""
    reducedIndividual = [0]
    j = 0        
    for i in range(len(individual)):
        reducedIndividual[j] += individual[i]
        if((i+1)%windowSize == 0 and (i+1) != len(individual)):
            j += 1
            reducedIndividual.append(0)
    return reducedIndividual

def WindowizeGroup(group,windowSize):
    """Goes through each individual in a group and educes their size by summing
    the number of mutations in a window and replacing all values with that sum."""
    windowedGroup = []    
    for i in range(len(group)):
        windowedGroup.append(Windowize(windowSize,group[i]))
    return windowedGroup

def WriteResultsToReport(result,fileName):
    """ write group as a csv to file"""
    try:
        with open(fileName,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)
    except:
        print("*****ERROR******")
        with open(fileName,'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(result)
            
def mutationPositions(n,individualSize):
    """n = (number of mutations) """
    positions = set()
    random.seed()
    while(len(positions) < n):
      	positions.add(random.randint(0, individualSize-1))
    return list(positions)
    
def RunMeasures(yTest,yPredictedBin):
    """Runs roc_auc_score on the predicted data in order to determine 
    the quality of fit the classification method produced"""
    try:
        roc_auc_score = metrics.roc_auc_score(yTest,yPredictedBin)
        results = [roc_auc_score]
    except:
        results = ["A Measure in RunMeasures failed"]
    return results
