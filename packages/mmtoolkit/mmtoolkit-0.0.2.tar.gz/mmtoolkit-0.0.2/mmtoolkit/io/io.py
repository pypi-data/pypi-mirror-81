import numpy as np
import os
from ..rotation import rotations


class dream3dIO(object):

    def __init__(self, projectName, xDim, yDim, zDim, wd):
        self.projectName = projectName
        self.xDim = xDim
        self.yDim = yDim
        self.zDim = zDim
        self.wd = wd
        self.indexArray = np.arange(xDim * yDim * zDim).reshape(zDim, yDim, xDim)

    @property
    def loadINL(self):
        self.d3dArray = np.loadtxt(os.path.join(self.wd, '{}.txt'.format(self.projectName)), comments='#')[:, :-3]

    @property
    def loadSPK(self):
        self.featureArray = np.loadtxt(os.path.join(self.wd, '{}.spparks'.format(self.projectName)), skiprows=9).astype(
            int)[:, 1]

    def loadCSV(self, skipRows=0, columnNum=0):
        self.featureArray = np.loadtxt(os.path.join(self.wd, '{}.spparks'.format(self.projectName)),
                                       skiprows=skipRows).astype(
            int)[:, columnNum]

    @property
    def closeArray(self):

        if isinstance(self.d3dArray, np.ndarray):
            self.d3dArray = None
            del self.d3dArray
        else:
            pass

        if isinstance(self.featureArray, np.ndarray):
            self.featureArray = None
            del self.featureArray
        else:
            pass

    def slice(self, numSlice=10, sliceType='uniform', onlyZ=True, sortIndex=False):

        os.makedirs(os.path.join(self.wd, 'slice'), exist_ok=True)
        self.sliceDir = os.path.join(self.wd, 'slice')

        # SLICING Z
        if sliceType == 'uniform':
            tempIndex = np.linspace(4, self.zDim - 5, num=numSlice, dtype=int)
        else:
            tempIndex = np.sort(np.random.choice(range(self.zDim), numSlice, replace=False))
        tempSliceIdx = self.indexArray[tempIndex].reshape(numSlice, -1)
        np.savetxt(os.path.join(self.sliceDir, '{}_sliceIdx_z.csv'.format(self.projectName)), tempSliceIdx,
                   fmt='%d',
                   delimiter='\t')
        if not onlyZ:
            # SLICING X
            if sliceType == 'uniform':
                tempIndex = np.linspace(4, self.xDim - 5, num=numSlice, dtype=int)
            else:
                tempIndex = np.sort(np.random.choice(range(self.xDim), numSlice, replace=False))
            tempSliceIdx = np.transpose(self.indexArray[:, :, tempIndex], (2, 1, 0)).reshape(numSlice, -1)
            if sortIndex:
                tempSliceIdx = np.sort(tempSliceIdx)
            else:
                pass
            np.savetxt(os.path.join(self.sliceDir, '{}_sliceIdx_x.csv'.format(self.projectName)), tempSliceIdx,
                       fmt='%d',
                       delimiter='\t')

            # SLICING Y
            if sliceType == 'uniform':
                tempIndex = np.linspace(4, self.yDim - 5, num=numSlice, dtype=int)
            else:
                tempIndex = np.sort(np.random.choice(range(self.yDim), numSlice, replace=False))
            tempSliceIdx = np.transpose(self.indexArray[:, tempIndex, :], (1, 2, 0)).reshape(numSlice, -1)

            if sortIndex:
                tempSliceIdx = np.sort(tempSliceIdx)
            else:
                pass
            np.savetxt(os.path.join(self.sliceDir, '{}_sliceIdx_y.csv'.format(self.projectName)), tempSliceIdx,
                       fmt='%d',
                       delimiter='\t')
        else:
            pass

    def getEuler(self, numSlice=10, onlyZ=True):

        # GETTING Z SLICES
        tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_sliceIdx_z.csv'.format(self.projectName)),
                                  delimiter='\t', dtype=int)
        tempOriArray = self.d3dArray[tempSliceIdx]
        for i in range(numSlice):
            np.savetxt(os.path.join(self.sliceDir, '{}_z_slice{}.csv'.format(self.projectName, i + 1)), tempOriArray[i],
                       fmt='%1.4f',
                       delimiter='\t')
        if not onlyZ:
            # GETTING X SLICES
            tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_sliceIdx_x.csv'.format(self.projectName)),
                                      delimiter='\t').astype(int)
            tempOriArray = self.d3dArray[tempSliceIdx]
            for i in range(numSlice):
                np.savetxt(os.path.join(self.sliceDir, '{}_x_slice{}.csv'.format(self.projectName, i + 1)),
                           tempOriArray[i],
                           fmt='%1.4f',
                           delimiter='\t')

            # GETTING Y SLICES
            tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_sliceIdx_y.csv'.format(self.projectName)),
                                      delimiter='\t').astype(int)
            tempOriArray = self.d3dArray[tempSliceIdx]
            for i in range(numSlice):
                np.savetxt(os.path.join(self.sliceDir, '{}_y_slice{}.csv'.format(self.projectName, i + 1)),
                           tempOriArray[i],
                           fmt='%1.4f',
                           delimiter='\t')
        else:
            pass

    def getFeature(self, numSlice=10, onlyZ=True):
        # GETTING Z SLICES
        tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_sliceIdx_z.csv'.format(self.projectName)),
                                  delimiter='\t').astype(int)
        tempFtArray = self.featureArray[tempSliceIdx]

        for i in range(numSlice):
            tempArray = tempFtArray[i]
            tempArray[np.where(tempArray == 2)] = 0
            np.savetxt(os.path.join(self.sliceDir, '{}_ft_z_slice{}.csv'.format(self.projectName, i + 1)), tempArray,
                       fmt='%d',
                       delimiter='\t')
        if not onlyZ:
            # GETTING X SLICES
            tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_sliceIdx_x.csv'.format(self.projectName)),
                                      delimiter='\t').astype(int)
            tempFtArray = self.featureArray[tempSliceIdx]
            for i in range(numSlice):
                tempArray = tempFtArray[i]
                tempArray[np.where(tempArray == 2)] = 0
                np.savetxt(os.path.join(self.sliceDir, '{}_ft_x_slice{}.csv'.format(self.projectName, i + 1)),
                           tempArray, fmt='%d', delimiter='\t')

            # GETTING Y SLICES
            tempSliceIdx = np.loadtxt(os.path.join(self.sliceDir, '{}_ft_sliceIdx_y.csv'.format(self.projectName)),
                                      delimiter='\t').astype(int)
            tempFtArray = self.featureArray[tempSliceIdx]
            for i in range(numSlice):
                tempArray = tempFtArray[i]
                tempArray[np.where(tempArray == 2)] = 0
                np.savetxt(os.path.join(self.sliceDir, '{}_y_slice{}.csv'.format(self.projectName, i + 1)),
                           tempArray,
                           fmt='%d',
                           delimiter='\t')
        else:
            pass

    def ctfWriter(self, numSlice=10, onlyZ=True):
        # print('Writting CTF files for each slice...')
        os.makedirs(os.path.join(self.wd, 'ctf'), exist_ok=True)
        self.ctfDir = os.path.join(self.wd, 'ctf')

        for i in range(numSlice):

            # Z SLICES
            tempOriArray = np.loadtxt(os.path.join(self.sliceDir, '{}_z_slice{}.csv'.format(self.projectName, i + 1)),
                                      delimiter='\t')
            ctfOriArray = np.ones((tempOriArray.shape[0], 11))
            ctfOriArray[:, 1:3] = tempOriArray[:, 3:5]
            ctfOriArray = dream3dIO.ctfArrayConverter(tempOriArray, ctfOriArray)
            f = open(os.path.join(self.ctfDir, '{}_z_slice{}.ctf'.format(self.projectName, i + 1)), 'w', newline='\n')
            dream3dIO.ctfFormatWritter(f, ctfOriArray)

            if not onlyZ:
                # X SLICES
                tempOriArray = np.loadtxt(
                    os.path.join(self.sliceDir, '{}_x_slice{}.csv'.format(self.projectName, i + 1)),
                    delimiter='\t')
                ctfOriArray = np.ones((tempOriArray.shape[0], 11))
                ctfOriArray[:, 1:3] = tempOriArray[:, 4:]
                ctfOriArray = dream3dIO.ctfArrayConverter(tempOriArray, ctfOriArray)
                f = open(os.path.join(self.ctfDir, '{}_x_slice{}.ctf'.format(self.projectName, i + 1)), 'w',
                         newline='\n')
                dream3dIO.ctfFormatWritter(f, ctfOriArray)

                # Y SLICES
                tempOriArray = np.loadtxt(
                    os.path.join(self.sliceDir, '{}_y_slice{}.csv'.format(self.projectName, i + 1)),
                    delimiter='\t')
                ctfOriArray = np.ones((tempOriArray.shape[0], 11))
                ctfOriArray[:, 1:3] = tempOriArray[:, [3, 5]]
                ctfOriArray = dream3dIO.ctfArrayConverter(tempOriArray, ctfOriArray)
                f = open(os.path.join(self.ctfDir, '{}_y_slice{}.ctf'.format(self.projectName, i + 1)), 'w',
                         newline='\n')
                dream3dIO.ctfFormatWritter(f, ctfOriArray)
            else:
                pass

    @staticmethod
    def ctfArrayConverter(tempOriArray, ctfOriArray):
        ctfOriArray[:, 3] = 8
        ctfOriArray[:, 4] = 0
        ctfOriArray[:, 5:8] = tempOriArray[:, :3] * 180 / np.pi
        ctfOriArray[:, 8] = np.random.uniform(0, 0.5, ctfOriArray.shape[0])
        ctfOriArray[:, 9] = np.random.randint(100, 150, ctfOriArray.shape[0])
        ctfOriArray[:, 10] = np.random.randint(150, 200, ctfOriArray.shape[0])
        return ctfOriArray

    @staticmethod
    def ctfFormatWritter(f, ctfOriArray):
        print('Channel Text File', file=f)
        print('Phases	1', file=f)
        print(
            '3.570;3.570;3.570	90.000;90.000;90.000	Ni-superalloy	11	225			Generic superalloy',
            file=f)
        print('Phase	X	Y	Bands	Error	Euler1	Euler2	Euler3	MAD	BC	BS', file=f)
        np.savetxt(f, ctfOriArray, encoding='utf-8',
                   fmt='%d\t%1.1f\t%1.1f\t%d\t%d\t%1.4f\t%1.4f\t%1.4f\t%1.4f\t%d\t%d')
        f.close()


class spparksIO(object):

    def __init__(self, **kwargs):
        self.wd = kwargs.get('wd', os.getcwd())

    def clusterReader(self, **kwargs):
        fileName = kwargs.get('fileName', '')

        os.makedirs(os.path.join(self.wd, 'cluster'), exist_ok=True)
        clusterDir = os.path.join(self.wd, 'cluster')

        timeArray = np.empty(0)
        numClusterArray = np.empty(0)
        meanVolArray = np.empty(0)
        meanCubicRadiusArray = np.empty(0)

        f = open(os.path.join(self.wd, '{}.cluster'.format(fileName)), 'r')
        for line in f:
            if 'Time' in line.split():
                timeArray = np.append(timeArray, np.asarray(line.split()[-1], dtype=np.float))
            elif 'ncluster' in line.split():
                numClusterArray = np.append(numClusterArray, np.asarray(line.split()[-1], dtype=np.int))
            elif '<N>' in line.split():
                meanVolArray = np.append(meanVolArray, np.asarray(line.split()[-1], dtype=np.float))
            elif '<R>' in line.split():
                meanCubicRadiusArray = np.append(meanCubicRadiusArray, np.asarray(line.split()[-1], dtype=np.float))

        timeArray = timeArray.reshape(-1, 1)
        numClusterArray = numClusterArray.reshape(-1, 1)
        meanVolArray = meanVolArray.reshape(-1, 1)
        meanCubicRadiusArray = meanCubicRadiusArray.reshape(-1, 1)
        meanSphereRadiusArray = np.cbrt(meanVolArray * 3 / (4 * np.pi))

        clusterArray = np.hstack(
            (timeArray, numClusterArray, meanVolArray, meanCubicRadiusArray, meanSphereRadiusArray))

        np.savetxt(os.path.join(clusterDir, '{}_cluster.csv'.format(fileName)), clusterArray, delimiter='\t',
                   fmt='%1.3f')

        return clusterArray


class ctfWriter(object):

    def __init__(self, **kwargs):
        self.wd = kwargs.get('wd', os.getcwd())
        os.makedirs(os.path.join(self.wd, 'ctf'), exist_ok=True)
        self.ctfDir = os.path.join(self.wd, 'ctf')

    def genOrientation(self, **kwargs):
        fileName = kwargs.get('fileName', '')
        fmt = kwargs.get('fmt', 'csv')
        usecols = kwargs.get('usecols', 0)

        featArray = np.loadtxt(os.path.join(self.wd, '{}.{}'.format(fileName, fmt)), usecols=usecols, dtype=int)

        uniFeature = np.unique(featArray)
        _n = uniFeature.size
        _randq = rotations.randQuats(_n)

        oriArray = np.ones((featArray.size, 3))

        for i in range(_n):
            oriArray[np.where(featArray == uniFeature[i])] = rotations.quat2euler(_randq[:, i])

        return oriArray

    def loadPosition(self, **kwargs):
        fileName = kwargs.get('fileName', '')
        fmt = kwargs.get('fmt', 'csv')
        usecols = kwargs.get('usecols', 0)

        positionArray = np.loadtxt(os.path.join(self.wd, '{}.{}'.format(fileName, fmt)), usecols=usecols)

        return positionArray

    def writeCTF(self, **kwargs):
        oriArray = kwargs.get('ori', np.ones((1, 3)))
        positionArray = kwargs.get('pos', np.ones((1, 2)))
        orifmt = kwargs.get('orifmt', 'deg')
        fileName = kwargs.get('fileName', '')

        ctfArray = np.zeros((oriArray.shape[0], 11))

        ctfArray[:, 0] = 1
        ctfArray[:, 1:3] = positionArray
        ctfArray[:, 3] = 8
        ctfArray[:, 4] = 0
        if orifmt == 'rad':
            ctfArray[:, 5:8] = oriArray * 180 / np.pi
        else:
            ctfArray[:, 5:8] = oriArray
        ctfArray[:, 8] = np.random.uniform(0, 0.5, oriArray.shape[0])
        ctfArray[:, 9] = np.random.randint(100, 150, oriArray.shape[0])
        ctfArray[:, 10] = np.random.randint(150, 200, oriArray.shape[0])

        # WRITE FILES
        f = open(os.path.join(self.ctfDir, '{}.ctf'.format(fileName)), 'w',
                 newline='\n')
        print('Channel Text File', file=f)
        print('Phases	1', file=f)
        print(
            '3.570;3.570;3.570	90.000;90.000;90.000	Ni-superalloy	11	225			Generic superalloy',
            file=f)
        print('Phase	X	Y	Bands	Error	Euler1	Euler2	Euler3	MAD	BC	BS', file=f)
        np.savetxt(f, ctfArray, encoding='utf-8',
                   fmt='%d\t%1.1f\t%1.1f\t%d\t%d\t%1.4f\t%1.4f\t%1.4f\t%1.4f\t%d\t%d')
        f.close()
