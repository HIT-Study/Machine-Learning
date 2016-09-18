# -*- coding: utf-8 -*-

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


def createC1(dataSet):
    C1 = []
    # C1 用来存储所有不重复的项值
    for transcation in dataSet:
        for item in transcation:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)  # 对C1中的每一个项构建一个不变的集合


def scanD(D, Ck, minSupport):
    '''
    该函数用于从C1生成L1
    :param D:数据集
    :param Ck:候选集列表
    :param minSupport:感兴趣项集的最小支持度
    '''
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData


if __name__ == '__main__':
    dataSet = loadDataSet()
    # print dataSet
    C1 = createC1(dataSet)
    # print C1
    D = map(set, dataSet)
    print D
    L1, suppData0 = scanD(D, C1, 0.5)
    print L1
