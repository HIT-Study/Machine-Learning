# -*- coding: utf-8 -*-
from math import log
import operator


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def calcShannonEnt(dataSet):
    '''
    计算给定数据集的香农熵
    '''
    sum = len(dataSet)
    labels = {}
    for data in dataSet:
        currentLabel = data[-1]
        if currentLabel not in labels.keys():
            labels[currentLabel] = 0
        labels[currentLabel] += 1
    shannonEnt = 0.0
    for key in labels:
        prob = float(labels[key]) / sum
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def splitDataSet(dataSet, axis, value):
    '''
    按照给定的特征划分数据集
    :param dataSet:
    :param axis:划分数据集的特征
    :param value:需要返回的特征的值
    :return:
    '''
    retDataSet = []
    for data in dataSet:
        if data[axis] == value:
            reducedFeatVec = data[:axis]
            reducedFeatVec.extend(data[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


if __name__ == '__main__':
    myData, labels = createDataSet()
    splitDataSet(myData, 0, 1)


def chooseBestFeatureToSplit(dataSet):
    '''选择最好的数据集的划分方式'''
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    '''多数表决'''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount
