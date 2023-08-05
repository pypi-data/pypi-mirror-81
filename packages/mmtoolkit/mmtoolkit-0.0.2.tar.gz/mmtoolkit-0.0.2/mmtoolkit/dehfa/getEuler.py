import numpy as np
import os
from rotations import triad

"""
r @ u = v
r is 3 by 3 rotation matrix
u can be extracted from SDV
v can be chose from slip systems
DEFAULT SETTING:
u = [[SDV37, SDV38, SDV39], [SDV73, SDV74, SDV75]].T
v = [[111], [0-11]].T
u and v are column vectors！

Modify the source code accordingly if you want to change the default setting of vector sets.
"""

os.chdir(r'D:\abqDirect\projects\3d_com_t01_1\results')
outd = os.getcwd()
odbName = '3d_com_t01_1'

# Read step information
stepInfo = np.genfromtxt('{}_STEP.csv'.format(odbName), dtype=None).reshape(-1, 2)
numStep = stepInfo.shape[0]
frameInfo = stepInfo[:, 1]

# Generating vector sets
v = np.array([[1, 1, 1], [0, -1, 1]])
v = v.T
v = v / np.linalg.norm(v, axis=0)
u = np.zeros([3, 2])

for i in range(numStep):
    numFrame = frameInfo[i]
    print('------------------------------------------------------------')
    print('STEP{} has {} FRAMES in total'.format(i + 1, numFrame))
    print('Operation on FRAME 1 has been skipped')
    print('------------------------------------------------------------')
    for j in range(1, numFrame):
        for k in range(3):
            tempArray1 = np.loadtxt('{}_SDV{}_s{}_f{}.csv'.format(odbName, 37 + k, i + 1, j + 1)).reshape(1, -1)
            tempArray2 = np.loadtxt('{}_SDV{}_s{}_f{}.csv'.format(odbName, 73 + k, i + 1, j + 1)).reshape(1, -1)
            if k == 0:
                slipNorm = tempArray1
                slipDir = tempArray2
            else:
                slipNorm = np.concatenate((slipNorm, tempArray1), axis=0)
                slipDir = np.concatenate((slipDir, tempArray2), axis=0)
            k += 1

        numIter = slipNorm.shape[1]
        oriArray = np.zeros([numIter, 16])

        for it in range(numIter):
            u[:, 0] = slipNorm[:, it]
            u[:, 1] = slipDir[:, it]
            t = triad(u, v)
            r = t.calcRot
            q = t.mat2quat
            euler = t.mat2euler
            oriArray[it, :4] = q
            oriArray[it, 4:13] = r.reshape(1, -1)
            oriArray[it, 13:] = euler

        np.savetxt(os.path.join(outd, '{}_ORI_s{}_f{}.csv'.format(odbName, i + 1, j + 1)), oriArray, fmt='%1.5f',
                   delimiter='\t')
        print('Euler angles from STEP{} FRAME{} has been saved'.format(i + 1, j + 1))
        j += 1
    i += 1

print('Program finished')
