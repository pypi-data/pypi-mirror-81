import numpy as np
import os
from sklearn.decomposition import PCA
from .optht import optht


class pca(object):

    def __init__(self, **kwargs):
        self.wd = kwargs.get('wd', os.getcwd())

        os.makedirs(os.path.join(self.wd, 'pca'), exist_ok=True)
        self.pcaDir = os.path.join(self.wd, 'pca')

    def compute(self, **kwargs):
        numComponents = kwargs.get('numComponents', 30)
        x = kwargs.get('x', np.random.random((10, 10)))
        fileName = kwargs.get('fileName', '')

        p = PCA(n_components=numComponents)
        x_new = p.fit_transform(x)
        numComponents = p.n_components

        f = open(os.path.join(self.pcaDir, '{}-pca-n.txt'.format(fileName)), 'w', newline='\n')
        print(numComponents, file=f)
        f.close()

        # SAVING STATISTICS
        np.savetxt(os.path.join(self.pcaDir, '{}-pca-xnew.txt'.format(fileName)), x_new, fmt='%1.5f',
                   delimiter='\t')
        np.savetxt(os.path.join(self.pcaDir, '{}-pca-components.txt'.format(fileName)), p.components_[:numComponents], fmt='%1.5f',
                   delimiter='\t')
        np.savetxt(os.path.join(self.pcaDir, '{}-pca-mean.txt'.format(fileName)), p.mean_, fmt='%1.5f',
                   delimiter='\t')
        np.savetxt(os.path.join(self.pcaDir, '{}-pca-varratio.txt'.format(fileName)), p.explained_variance_ratio_, fmt='%1.5f',
                   delimiter='\t')
        np.savetxt(os.path.join(self.pcaDir, '{}-pca-var.txt'.format(fileName)), p.explained_variance_, fmt='%1.5f',
                   delimiter='\t')
        np.savetxt(os.path.join(self.pcaDir, '{}-pca-sv.txt'.format(fileName)), p.singular_values_, fmt='%1.5f',
                   delimiter='\t')



