# -*- coding: utf-8 -*-
from numpy import *
import operator


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


# 此处写出kNN算法的伪代码：
# 1.对新数据，分别计算点和训练集中的各点之间的距离；
# 2.按照距离进行递增次序排序；
# 3.选择与当前距离最小的K个点；
# 4.确定前k个点中各个分类出现的频率；
# 5.返回前k个点钟分类频率最高的点的类别作为预测分类

def kNNClassify(input, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(input, (dataSetSize, 1)) - dataSet  # tile的功能是：重复input至 (dataSet,1)维度
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)  # axis=1的作用是把矩阵的每一行向量相加。 如[1,2] => 3
    distances = sqDistances ** 0.5
    # -----距离计算完毕-----#
    sortedDistIndicies = distances.argsort()  # argsort函数返回的是数组值从小到大的索引值
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    '''
    把文件转换成易于计算的矩阵
    '''
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()  # 删除所有的回车符
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]  # return[1,:]代表第一行所有元素
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    '''归一化特征值
    公式 : newValue = (oldValue - min)/(max - min)
    '''
    minVals = dataSet.min(0)  # 参数0 使得函数可以从列中选取最小值
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]  # 样本总行数
    numTestVecs = int(m * hoRatio)  # 测试集的数量
    errorCount = 0.0
    for i in range(numTestVecs):
        classifyResult = kNNClassify(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print "the classifyResult came back with :%d, the real answer is :%d" % (classifyResult, datingLabels[i])
        if (classifyResult != datingLabels[i]):
            errorCount += 1.0
    print "the total error rate is :%f" % (errorCount / float(numTestVecs))


def img2Vector(filename):
    '''
    将32*32的二进制图片矩阵转换成1*1024的向量
    '''
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect


