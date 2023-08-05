import numpy as np
import os
import sys


class hexGridSlicer(object):

    def __init__(self, **kwargs):

        self.wd = kwargs.get('wd', os.getcwd())
        self.xDim = kwargs.get('xDim', 128)
        self.yDim = kwargs.get('yDim', 128)
        self.zDim = kwargs.get('zDim', 128)
        self.indexArray = np.arange(self.xDim * self.yDim * self.zDim).reshape((self.zDim, self.yDim, self.xDim))

        os.makedirs(os.path.join(self.wd, 'slice'), exist_ok=True)
        self.sliceDir = os.path.join(self.wd, 'slice')

    def genSliceIndex(self, **kwargs):
        print('正在获取切切分面索引......')
        fileName = kwargs.get('fileName', '')
        numSlice = kwargs.get('numSlice', 10)
        sliceType = kwargs.get('sliceType', 'uniform')
        sliceDirection = kwargs.get('sliceDirection', ['x', 'y', 'z'])
        sortIndex = kwargs.get('sortIndex', False)
        skipBoundary = kwargs.get('skipBoundary', 4)
        sliceIndex = kwargs.get('sliceIndex', [])

        if 'x' in sliceDirection or 'y' in sliceDirection or 'z' in sliceDirection:
            # SLICING Z
            if 'z' in sliceDirection:
                if sliceType == 'uniform':
                    tempIndex = np.linspace(skipBoundary, self.zDim - skipBoundary - 1, num=numSlice, dtype=int)
                elif sliceType == 'list':
                    tempIndex = sliceIndex
                    numSlice = len(tempIndex)
                else:
                    tempIndex = np.sort(np.random.choice(range(self.zDim), numSlice, replace=False))
                tempSliceIdx = self.indexArray[tempIndex].reshape(numSlice, -1)
                np.savetxt(os.path.join(self.sliceDir, '{}_slice_index_z.csv'.format(fileName)), tempSliceIdx,
                           fmt='%d',
                           delimiter='\t')

            if 'y' in sliceDirection:
                # SLICING Y
                if sliceType == 'uniform':
                    tempIndex = np.linspace(skipBoundary, self.yDim - skipBoundary - 1, num=numSlice, dtype=int)
                elif sliceType == 'list':
                    tempIndex = sliceIndex
                    numSlice = len(tempIndex)
                else:
                    tempIndex = np.sort(np.random.choice(range(self.yDim), numSlice, replace=False))
                tempSliceIdx = np.transpose(self.indexArray[:, tempIndex, :], (1, 2, 0)).reshape(numSlice, -1)

                if sortIndex:
                    tempSliceIdx = np.sort(tempSliceIdx)
                else:
                    pass
                np.savetxt(os.path.join(self.sliceDir, '{}_slice_index_y.csv'.format(fileName)), tempSliceIdx,
                           fmt='%d',
                           delimiter='\t')

            if 'x' in sliceDirection:
                # SLICING X
                if sliceType == 'uniform':
                    tempIndex = np.linspace(skipBoundary, self.xDim - skipBoundary - 1, num=numSlice, dtype=int)
                elif sliceType == 'list':
                    tempIndex = sliceIndex
                    numSlice = len(tempIndex)
                else:
                    tempIndex = np.sort(np.random.choice(range(self.xDim), numSlice, replace=False))
                tempSliceIdx = np.transpose(self.indexArray[:, :, tempIndex], (2, 1, 0)).reshape(numSlice, -1)
                if sortIndex:
                    tempSliceIdx = np.sort(tempSliceIdx)
                else:
                    pass
                np.savetxt(os.path.join(self.sliceDir, '{}_slice_index_x.csv'.format(fileName)), tempSliceIdx,
                           fmt='%d',

                           delimiter='\t')
        else:
            print('输入切分方向错误')
            sys.exit(0)

    def getFeature(self, **kwargs):
        print('正在导出切分面特征值......')
        fmt = kwargs.get('fmt', 'spparks')
        usecols = kwargs.get('usecols', 1)
        skiprows = kwargs.get('skiprows', 9)
        fileName = kwargs.get('fileName', '')
        sliceDirection = kwargs.get('sliceDirection', ['x', 'y', 'z'])
        renameFeature = kwargs.get('renameFeature', 512)
        sortArray = kwargs.get('sortArray', False)

        if sortArray:
            featureArray = np.loadtxt(os.path.join(self.wd, '{}.{}'.format(fileName, fmt)), skiprows=skiprows)
            featureArray = featureArray[featureArray[:, 0].argsort()]
            if type(usecols) is int:
                featureArray = featureArray[:, usecols].astype(int)
            else:
                featureArray = featureArray[:, usecols]

        else:
            if type(usecols) is int:
                featureArray = np.loadtxt(os.path.join(self.wd, '{}.{}'.format(fileName, fmt)), skiprows=skiprows,
                                          usecols=usecols, dtype=int)
            else:
                featureArray = np.loadtxt(os.path.join(self.wd, '{}.{}'.format(fileName, fmt)), skiprows=skiprows,
                                          usecols=usecols)

        if 'x' in sliceDirection or 'y' in sliceDirection or 'z' in sliceDirection:

            # SLICING Z
            if 'z' in sliceDirection:
                tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_slice_index_z.csv'.format(fileName)),
                                          delimiter='\t', dtype=int)
                if isinstance(tempSliceIdx[0], list):
                    numSlice = tempSliceIdx.shape[0]
                else:
                    numSlice = 1
                tempFtArray = featureArray[tempSliceIdx]

                for i in range(numSlice):
                    if numSlice == 1:
                        tempArray = tempFtArray
                    else:
                        tempArray = tempFtArray[i]
                    if renameFeature:
                        tempArray[np.where(tempArray <= renameFeature)] = 1
                        tempArray[np.where(tempArray > renameFeature)] = 0

                    if numSlice == 1:
                        np.savetxt(os.path.join(self.sliceDir, '{}_ft_slice_z.csv'.format(fileName)),
                                   tempArray,
                                   fmt='%1.3f', delimiter='\t')
                    else:
                        np.savetxt(os.path.join(self.sliceDir, '{}_ft_slice_z_{}.csv'.format(fileName, i + 1)),
                                   tempArray, fmt='%d', delimiter='\t')

            if 'y' in sliceDirection:
                # GETTING Y SLICES
                tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_slice_index_y.csv'.format(fileName)),
                                          delimiter='\t', dtype=int)
                if isinstance(tempSliceIdx[0], list):
                    numSlice = tempSliceIdx.shape[0]
                else:
                    numSlice = 1
                tempFtArray = featureArray[tempSliceIdx]

                for i in range(numSlice):
                    if numSlice == 1:
                        tempArray = tempFtArray
                    else:
                        tempArray = tempFtArray[i]

                    if renameFeature:
                        tempArray[np.where(tempArray <= renameFeature)] = 1
                        tempArray[np.where(tempArray > renameFeature)] = 0

                    if numSlice == 1:
                        np.savetxt(os.path.join(self.sliceDir, '{}_ft_slice_y.csv'.format(fileName)),
                                   tempArray,
                                   fmt='%1.3f', delimiter='\t')
                    else:
                        np.savetxt(os.path.join(self.sliceDir, '{}_ft_slice_y_{}.csv'.format(fileName, i + 1)),
                                   tempArray, fmt='%d', delimiter='\t')

            if 'x' in sliceDirection:
                # GETTING X SLICES
                tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_slice_index_x.csv'.format(fileName)),
                                          delimiter='\t', dtype=int)
                if isinstance(tempSliceIdx[0], list):
                    numSlice = tempSliceIdx.shape[0]
                else:
                    numSlice = 1
                tempFtArray = featureArray[tempSliceIdx]

                for i in range(numSlice):
                    if numSlice == 1:
                        tempArray = tempFtArray
                    else:
                        tempArray = tempFtArray[i]

                    if renameFeature:
                        tempArray[np.where(tempArray <= renameFeature)] = 1
                        tempArray[np.where(tempArray > renameFeature)] = 0
                    else:
                        pass

                    if numSlice == 1:
                        np.savetxt(os.path.join(self.sliceDir, '{}_ft_slice_x.csv'.format(fileName)),
                                   tempArray,
                                   fmt='%1.3f', delimiter='\t')
                    else:
                        np.savetxt(os.path.join(self.sliceDir, '{}_ft_slice_x_{}.csv'.format(fileName, i + 1)),
                                   tempArray, fmt='%d', delimiter='\t')
        else:
            print('输入切分方向错误')
            sys.exit(0)

    def getEuler(self, **kwargs):
        pass
