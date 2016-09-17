# -*- coding: utf-8 -*-

from numpy import *


def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat


def distEclud(vecA, vecB):
    '''计算两个向量之间的欧氏距离'''
    return sqrt(sum(power(vecA - vecB, 2)))


def randCent(dataSet, k):
    '''该函数为给定的数据集构建一个包含k个随机质心的集合'''
    n = shape(dataSet)[1]  # n是数据集的列数
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataMat[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    '''
    该算法会创建k个质心，然后将每个点分配到最近的质心，再重新计算质心。
    '''
    m = shape(dataMat)[0]  # 数据集的行数
    clusterAssment = mat(zeros((m, 2)))  # 记录簇分配结果,一列记录簇索引值，第二列存储误差
    centroids = createCent(dataSet, k)  # 随机初始质心
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j  # 寻找最近的质心
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        print centroids
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]  # 更新质心位置
            centroids[cent, :] = mean(ptsInClust, axis=0)  # axis = 0 表示沿矩阵的列方向进行均值计算
    return centroids, clusterAssment


if __name__ == '__main__':
    dataMat = mat(loadDataSet('testSet.txt'))
    myCentroids, clustAssing = kMeans(dataMat, 4)
    # print myCentroids
    # print "---------------"
    # print clustAssing
