import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
import os
import numpy as np
from scipy.interpolate import interp1d


class plots(object):

    def __init__(self, **kwargs):
        self.save = kwargs.get('save', False)
        self.wd = kwargs.get('wd', None)
        self.fileName = kwargs.get('fileName', None)
        self.dpi = kwargs.get('dpi', None)

    def imagePlot(self, **kwargs):
        plt.rcParams['figure.figsize'] = [10, 8]
        plt.rcParams.update({'font.size': 18})
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = 'Lato'

        cmap = kwargs.get('cmap', 'viridis')
        interpolation = kwargs.get('interpolation', None)
        vmax = kwargs.get('vmax', None)
        vmin = kwargs.get('vmin', None)
        x = kwargs.get('x', np.ones((10, 10)))
        cbartitle = kwargs.get('cbartitle', None)
        title = kwargs.get('title', None)

        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        im = ax.imshow(x, extent=[-x.shape[1] / 2., x.shape[1] / 2., -x.shape[0] / 2., x.shape[0] / 2.],
                       interpolation=interpolation,
                       cmap=cmap, vmin=vmin, vmax=vmax)

        ax.minorticks_on()
        ax.tick_params(which='minor', direction='in', length=4)
        ax.tick_params(which='major', direction='in', length=8)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.minorticks_on()
        cbar.ax.tick_params(which='minor', direction='in', length=2)
        cbar.ax.tick_params(direction='in', length=4)

        if title:
            ax.set_title()

        if cbartitle:
            cbar.ax.get_yaxis().labelpad = 20
            cbar.ax.set_ylabel('{}'.format(cbartitle), rotation=270)

        if self.save:
            plt.savefig(os.path.join(self.wd, '{}.jpg'.format(self.fileName)), dpi=self.dpi)
        else:
            plt.show()

    def categoricalScatter(self, **kwargs):

        xnew = kwargs.get('x', np.ones((3, 3)))
        dim = kwargs.get('dim', 3)
        labels = kwargs.get('labels', '')
        cdict = kwargs.get('cdict', {})
        labelpad = kwargs.get('labelpad', 0)
        figuresize = kwargs.get('figuresize', [10, 8])
        xlim = kwargs.get('xlim', (None, None))
        ylim = kwargs.get('ylim', (None, None))
        zlim = kwargs.get('zlim', (None, None))
        xlabel = kwargs.get('xlabel', '')
        ylabel = kwargs.get('ylabel', '')
        zlabel = kwargs.get('zlabel', '')
        title = kwargs.get('title', '')

        plt.rcParams['figure.figsize'] = figuresize
        plt.rcParams.update({'font.size': 18})
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = 'Lato'
        plt.rcParams['scatter.edgecolors'] = 000000

        fig = plt.figure()

        if dim == 3:
            ax = Axes3D(fig)
            for label in np.unique(labels):
                i = np.where(labels == label)
                ax.scatter(xnew[i, 0], xnew[i, 1], xnew[i, 2], c=cdict[label], s=60, label=label, depthshade=False)

            ax.legend(loc='best')
            ax.set_xlabel("{}".format(xlabel))
            ax.set_ylabel("{}".format(ylabel))
            ax.set_zlabel("{}".format(zlabel))

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_ylim(zlim)

            ax.xaxis.labelpad = labelpad
            ax.yaxis.labelpad = labelpad
            ax.zaxis.labelpad = labelpad

            ax.set_title("{}".format(title))

        elif dim == 2:
            ax = plt.subplot()
            for label in np.unique(labels):
                i = np.where(labels == label)
                ax.scatter(xnew[i, 0], xnew[i, 1], c=cdict[label], s=60, label=label)

            ax.legend(loc='best')
            ax.set_xlabel("{}".format(xlabel))
            ax.set_ylabel("{}".format(ylabel))

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            fig.tight_layout()

        else:
            print('输入错误')

        if self.save:
            plt.savefig(os.path.join(self.wd, '{}.jpg'.format(self.fileName)), dpi=self.dpi)
        else:
            plt.show()

    def simpleLine(self, **kwargs):

        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        xlim = kwargs.get('xlim', (None, None))
        ylim = kwargs.get('ylim', (None, None))
        xlabel = kwargs.get('xlabel', '')
        ylabel = kwargs.get('ylabel', '')
        cmap = kwargs.get('cmap', None)

        fig, ax = plt.subplots()
        fig.tight_layout()

        ax.set_xlabel('{}'.format(xlabel))
        ax.set_ylabel('{}'.format(ylabel))

        if isinstance(y[0], list):
            if cmap is not None:
                for i in range(y.shape[1]):
                    ax.plot(x, y[:, i], color=cmap[i])
            else:
                for i in range(y.shape[1]):
                    ax.plot(x, y[:, i])

        else:
            ax.plot(x, y)

        ax.minorticks_on()
        ax.tick_params(which='minor', direction='in', length=4)
        ax.tick_params(which='major', direction='in', length=8)

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        plt.show()

    def arcld(self, **kwargs):

        xbin = kwargs.get('xbin', None)
        z = kwargs.get('z', None)
        cmap = kwargs.get('cmap', 'viridis')
        vmax = kwargs.get('vmax', None)
        vmin = kwargs.get('vmin', None)

        [r, t] = np.meshgrid(xbin, np.linspace(0, 2 * np.pi, num=360));
        x = r * np.cos(t)
        y = r * np.sin(t)

        arcldArray = np.vstack((z, z))
        fig, ax = plt.subplots()
        im = ax.contourf(x, y, arcldArray, 128, vmin=vmin, vmax=vmax, cmap=cmap)

        ax.set_aspect('equal')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.get_yaxis().labelpad = 20
        # cbar.ax.set_ylabel('PC3', rotation=270)
        
        if self.save:
            plt.savefig(os.path.join(self.wd, '{}.jpg'.format(self.fileName)), dpi=self.dpi)
        else:
            plt.show()
