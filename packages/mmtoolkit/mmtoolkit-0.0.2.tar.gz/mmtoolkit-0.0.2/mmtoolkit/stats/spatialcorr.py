import numpy as np
import dask.array as da
from sklearn.pipeline import Pipeline
from pymks import PrimitiveTransformer, TwoPointCorrelation
import os


class twopoints(object):

    def __init__(self, **kwargs):

        self.wd = kwargs.get('wd', os.getcwd())
        self.dataArray = np.array(())

        os.makedirs(os.path.join(self.wd, 'twopoints'), exist_ok=True)
        self.tpDir = os.path.join(self.wd, 'twopoints')

    def loadArray(self, **kwargs):
        xDim = kwargs.get('xDim', 128)
        yDim = kwargs.get('yDim', 128)
        zDim = kwargs.get('zDim', 1)
        arr = kwargs.get('arr', np.array(()))

        self.dataArray = da.from_array(arr.reshape((zDim, yDim, xDim)), chunks=(zDim, yDim, xDim)).persist()

    def loadDaskArray(self, **kwargs):
        arr = kwargs.get('arr', np.array(()))
        self.dataArray = arr

    def compute(self, **kwargs):

        pbc = kwargs.get('pbc', False)
        fileName = kwargs.get('fileName', '')

        model = Pipeline(steps=[
            ('discretize', PrimitiveTransformer(n_state=2, min_=0.0, max_=1.0)),
            ('correlations', TwoPointCorrelation(
                periodic_boundary=pbc,
                cutoff=self.dataArray.shape[1],
                correlations=[[0, 0], [1, 1], [0, 1]]
            ))
        ])

        statsArray = model.transform(self.dataArray).persist()
        zDim = statsArray.shape[0]

        if zDim == 1:
            np.savetxt(os.path.join(self.tpDir, '{}_corr0.csv'.format(fileName)),
                       statsArray[0, :, :, 0].compute(), fmt='%1.8f', delimiter='\t')
            np.savetxt(os.path.join(self.tpDir, '{}_corr1.csv'.format(fileName)),
                       statsArray[0, :, :, 1].compute(), fmt='%1.8f', delimiter='\t')
            np.savetxt(os.path.join(self.tpDir, '{}_corr2.csv'.format(fileName)),
                       statsArray[0, :, :, 2].compute(), fmt='%1.8f', delimiter='\t')
        else:
            for i in range(zDim):
                np.savetxt(os.path.join(self.tpDir, '{}_{}_corr0.csv'.format(fileName, i + 1)),
                           statsArray[i, :, :, 0].compute(), fmt='%1.8f', delimiter='\t')
                np.savetxt(os.path.join(self.tpDir, '{}_{}_corr1.csv'.format(fileName, i + 1)),
                           statsArray[i, :, :, 1].compute(), fmt='%1.8f', delimiter='\t')
                np.savetxt(os.path.join(self.tpDir, '{}_{}_corr2.csv'.format(fileName, i + 1)),
                           statsArray[i, :, :, 2].compute(), fmt='%1.8f', delimiter='\t')
