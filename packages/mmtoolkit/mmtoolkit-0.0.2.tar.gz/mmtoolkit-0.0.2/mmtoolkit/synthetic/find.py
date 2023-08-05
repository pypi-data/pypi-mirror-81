import os
import numpy as np
from scipy.spatial import cKDTree


class getWorkList(object):

    def __init__(self, odbName, cwd):
        self.odbName = odbName
        self.cwd = cwd

    @property
    def neighborElements(self):

        elementArray = np.loadtxt(os.path.join(self.cwd, '{}_ME.csv'.format(self.odbName)),
                                  delimiter='\t').astype(int)
        numElements = elementArray.shape[0]

        with open(os.path.join(self.cwd, '{}_NE.csv'.format(self.odbName)), 'ab') as f:
            f.seek(0)
            f.truncate(0)
            for i in range(numElements):
                tempWorkList = np.array([])
                nodeList = elementArray[i]
                testBoolean = np.array([elementArray == n for n in nodeList])
                for j in range(testBoolean.shape[2]):
                    tempList = np.where(testBoolean[j])[0]
                    if len(tempList) != 0:
                        tempWorkList = np.concatenate((tempWorkList, tempList), axis=0)
                    j += 1

                tempWorkList = np.unique(tempWorkList)
                tempWorkList = tempWorkList + 1
                tempWorkList = np.delete(tempWorkList, np.where(tempWorkList == i + 1))
                tempWorkList = tempWorkList.reshape(1, -1)

                np.savetxt(f, tempWorkList, fmt='%d', delimiter='\t')
                i += 1
            f.close()

    def neighborElementsKDTREE(self, k=8):
        centroidArray = np.loadtxt(os.path.join(self.cwd, '{}_COORD_EC.csv'.format(self.odbName)), delimiter='\t')
        tree = cKDTree(centroidArray)
        index = tree.query(centroidArray, k + 1)[1]
        index = index[:, 1:] + 1
        index = np.sort(index)
        np.savetxt(os.path.join(self.cwd, '{}_NEK.csv'.format(self.odbName)), index, fmt='%d',
                   delimiter='\t')

    def neighborNodesKDTREE(self, k=8):
        nodeArray = np.loadtxt(os.path.join(self.cwd, '{}_MN.csv'.format(self.odbName)), delimiter='\t')
        tree = cKDTree(nodeArray)
        index = tree.query(nodeArray, k + 1)[1]
        index = index[:, 1:] + 1
        index = np.sort(index)
        np.savetxt(os.path.join(self.cwd, '{}_NNK.csv'.format(self.odbName)), index, fmt='%d',
                   delimiter='\t')

    @property
    def neighborElesetE(self):
        elementArray = np.loadtxt(os.path.join(self.cwd, '{}_ME.csv'.format(self.odbName)),
                                  delimiter='\t').astype(int)
        elesetArray = np.loadtxt(os.path.join(self.cwd, '{}_MESET.csv'.format(self.odbName)),
                                 delimiter='\t').astype(int)
        numElements = elementArray.shape[0]

        with open(os.path.join(self.cwd, '{}_NESETE.csv'.format(self.odbName)), 'ab') as f:
            f.seek(0)
            f.truncate(0)
            for i in range(numElements):
                tempElesetNum = elesetArray[i]
                testBoolean = elesetArray == tempElesetNum
                tempWorkList = np.where(testBoolean)[0]
                tempWorkList = tempWorkList + 1
                tempWorkList = np.delete(tempWorkList, np.where(tempWorkList == i + 1))
                tempWorkList = tempWorkList.reshape(1, -1)
                # print(tempWorkList)
                np.savetxt(f, tempWorkList, fmt='%d', delimiter='\t')
                i += 1
        f.close()


    @property
    def neighborElesetN(self):
        elementArray = np.loadtxt(os.path.join(self.cwd, '{}_ME.csv'.format(self.odbName)),
                                  delimiter='\t').astype(int)
        elesetArray = np.loadtxt(os.path.join(self.cwd, '{}_MESET.csv'.format(self.odbName)),
                                 delimiter='\t').astype(int)
        numElements = elementArray.shape[0]

        with open(os.path.join(self.cwd, '{}_NESETE.csv'.format(self.odbName)), 'ab') as f:
            f.seek(0)
            f.truncate(0)
            for i in range(numElements):
                tempElesetNum = elesetArray[i]
                testBoolean = elesetArray == tempElesetNum
                tempWorkList = np.where(testBoolean)[0]
                tempWorkList = tempWorkList + 1
                tempWorkList = np.delete(tempWorkList, np.where(tempWorkList == i + 1))
                tempWorkList = tempWorkList.reshape(1, -1)
                # print(tempWorkList)
                np.savetxt(f, tempWorkList, fmt='%d', delimiter='\t')
                i += 1
        f.close()

    def getBoundaryNodes(self):

        pass

    @property
    def getElementCentroid(self):

        nodeArray = np.loadtxt(os.path.join(self.cwd, '{}_MN.csv'.format(self.odbName)), delimiter='\t')
        elementArray = np.loadtxt(os.path.join(self.cwd, '{}_ME.csv'.format(self.odbName)),
                                  delimiter='\t').astype(int)

        nodeDimension = nodeArray.shape[1]
        numElements = elementArray.shape[0]

        centroidCoord = np.empty((0, nodeDimension))
        for i in range(numElements):
            nodeList = elementArray[i]
            tempCentroidCoord = np.zeros((1, nodeDimension))
            numNodesElement = nodeList.shape[0]
            for n in nodeList:
                tempNodeCoord = nodeArray[n - 1, :]
                tempCentroidCoord += tempNodeCoord
            tempCentroidCoord = tempCentroidCoord / numNodesElement
            centroidCoord = np.concatenate((centroidCoord, tempCentroidCoord))

        np.savetxt(os.path.join(self.cwd, '{}_COORD_EC.csv'.format(self.odbName)), centroidCoord, fmt='%5f',
                   delimiter='\t')