import numpy as np
import os
from tqdm import trange
from ..numbajit import *


class moriElemental(object):

    def __init__(self, quatArray, odbName, cwd):
        self.quatArray = quatArray
        self.numIter = quatArray.shape[0]
        self.odbName = odbName
        self.cwd = cwd

    def calcKAM(self, stepNum, frameNum, method=1):

        lines = None
        workListTree = None
        workList = None
        if method == 1:
            f = open(os.path.join(self.cwd, '{}_NE.csv'.format(self.odbName)))
            lines = f.readlines()
            f.close()
        elif method == 2:
            workListTree = np.loadtxt(os.path.join(self.cwd, '{}_NEK.csv'.format(self.odbName)),
                                      delimiter='\t').astype(int)

        kamList = np.empty([0, 1])
        for i in trange(self.numIter):
            tempKAM = 0
            if method == 1:
                workList = lines[i]
                workList = np.fromstring(workList, dtype=int, sep='\t')
            if method == 2:
                workList = workListTree[i]

            numNeigh = len(workList)
            for j in workList:
                q1 = self.quatArray[i]
                q2 = self.quatArray[j - 1]
                quatSym1 = symmetriesCubic(q1)
                quatSym2 = symmetriesCubic(q2)
                mang = calcDisoriCubic(quatSym1, quatSym2)
                tempKAM += mang
            tempKAM = tempKAM / numNeigh
            kamList = np.vstack((kamList, tempKAM))

            # print('{}/{} KAM values has been calculated'.format(i + 1, self.numIter))

        np.savetxt(os.path.join(self.cwd, '{}_KAM_s{}_f{}.csv'.format(self.odbName, stepNum, frameNum)), kamList,
                   fmt='%1.3f',
                   delimiter='\t')

    def calcGAM(self, stepNum, frameNum):

        f = open(os.path.join(self.cwd, '{}_NESETE.csv'.format(self.odbName)))
        lines = f.readlines()
        f.close()

        gamList = np.empty([0, 1])

        for i in trange(self.numIter):
            tempGAM = 0
            workList = lines[i]
            workList = np.fromstring(workList, dtype=int, sep='\t')
            numNeigh = len(workList)

            for j in workList:
                q1 = self.quatArray[i]
                q2 = self.quatArray[j - 1]
                quatSym1 = symmetriesCubic(q1)
                quatSym2 = symmetriesCubic(q2)
                mang = calcDisoriCubic(quatSym1, quatSym2)
                tempGAM += mang

            tempGAM = tempGAM / numNeigh
            gamList = np.vstack((gamList, tempGAM))

        np.savetxt(os.path.join(self.cwd, '{}_GAM_s{}_f{}.csv'.format(self.odbName, stepNum, frameNum)), gamList,
                   fmt='%1.3f',
                   delimiter='\t')

    def calcGOS(self, stepNum, frameNum):

        elesetArray = np.loadtxt(os.path.join(self.cwd, '{}_MESET.csv'.format(self.odbName)), delimiter='\t')
        numEleset = np.unique(elesetArray).shape[0]

        gosList = np.zeros([self.numIter, 1])
        for i in trange(numEleset):
            tempGOS = 0
            testBoolean = elesetArray == i + 1
            workList = np.where(testBoolean)[0]
            numNeigh = len(workList)

            tempQuatArray = self.quatArray[workList]

            q2 = calcMeanOrientation(tempQuatArray)
            quatSym2 = symmetriesCubic(q2)

            for j in workList:
                q1 = self.quatArray[j]
                quatSym1 = symmetriesCubic(q1)
                mang = calcDisoriCubic(quatSym1, quatSym2)
                tempGOS += mang

            tempGOS = tempGOS / numNeigh
            gosList[workList] = tempGOS

        np.savetxt(os.path.join(self.cwd, '{}_GOS_s{}_f{}.csv'.format(self.odbName, stepNum, frameNum)), gosList,
                   fmt='%1.3f',
                   delimiter='\t')


class moriNodal(object):

    def __init__(self, quatArray, odbName, cwd):
        self.quatArray = quatArray
        self.numIter = quatArray.shape[0]
        self.odbName = odbName
        self.cwd = cwd


def calcMeanOrientation(_q):
    """
    input quaternion array should be in shape (*, 4)
    """
    return np.mean(_q, axis=0)
