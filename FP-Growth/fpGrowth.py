# -*- coding: utf-8 -*-

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print ' ' * ind, self.name, '   ', self.count
        for child in self.children.values():
            child.disp(ind + 1)


def updateTree(items, inTree, headerTable, count):
    '''FP树生长'''
    if items[0] in inTree.children:  # 首先测试事务中的第一个元素项是否作为子节点存在
        inTree.children[items[0]].inc(count)
    else:  # 不存在，创建一个新的treeNode并将其作为一个子节点添加到树中，这时，头结点也要更新以指向新的结点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:  # call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):  # this version does not use recursion
    '''确保节点链接指向树中该元素项的每一个实例'''
    while (nodeToTest.nodeLink != None):  # Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def createTree(dataSet, minSup=1):  # create FP-tree from dataset but don't mine
    '''使用数据集和最小支持度计数来构造FP树'''
    headerTable = {}  # go over dataSet twice
    for trans in dataSet:  # first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in headerTable.keys():  # remove items not meeting minSup
        if headerTable[k] < minSup:
            del (headerTable[k])  # 移除不满足最小支持度技术的元素项
    freqItemSet = set(headerTable.keys())
    # print 'freqItemSet: ',freqItemSet
    if len(freqItemSet) == 0: return None, None  # if no items meet min support -->get out
    for k in headerTable:  # 对头指针表稍加扩展就可以保存计数值和指向每种类型第一个元素的指针
        headerTable[k] = [headerTable[k], None]  # reformat headerTable to use Node link
    # print 'headerTable: ',headerTable
    retTree = treeNode('Null Set', 1, None)  # create tree
    for tranSet, count in dataSet.items():  # go through dataset 2nd time
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)  ## 使用排序后的频繁项集对树进行填充
    return retTree, headerTable  # return tree and header table


def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def ascendTree(leafNode, prefixPath):
    '''上溯FP树'''
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]  # (sort header table)
    # 程序首先对头指针表中的元素按照其出现的频率进行排序（默认顺序是从小到大）
    for basePat in bigL:  # start from bottom of header table
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        # print 'finalFrequent Item: ',newFreqSet    #append to set
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])  # 递归调用函数来创建条件基
        # print 'condPattBases :',basePat, condPattBases
        # 2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)
        # print 'head from conditional tree: ', myHead
        if myHead != None:  # 3. mine cond. FP-tree
            print 'conditional tree for: ', newFreqSet
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


if __name__ == '__main__':
    simpDat = loadSimpDat()
    print simpDat
    print "----------"
    initSet = createInitSet(simpDat)
    print initSet
    print "-----------------"
    myFPTree, myHeaderTab = createTree(initSet, 3)
    myFPTree.disp()
    print "---------------"
    condPats = findPrefixPath('x', myHeaderTab['x'][1])
    condPatsR = findPrefixPath('r', myHeaderTab['r'][1])
    print condPatsR
    freqItems = []
    mineTree(myFPTree, myHeaderTab, 3, set([]), freqItems)



