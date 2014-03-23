from __future__ import print_function, division, absolute_import
from mixtape.featurizer import featurize_all
from mixtape.cmdline import Command, argument, argument_group
from projector.pca import PCACommand

__all__ = ['tICACommand']


class tICACommand(PCACommand):
    name = 'tica'
    description = 'Compute 2D projection with time-structure independent components analyis (tICA)'

    g = argument_group('required arguments')
    g.add_argument('--featurizer', required=True, help='''Path to a featurizer
        pickle. These can be created with the 'hmsm featurizer' command in
        mixtape.''')
    g.add_argument('--offset', required=True, type=int, help='''Delay time
        forward or backward in the input data. tICA is based on time-lagged
        correlations is computed between frames X[t] and X[t+offset]. `offset`
        is interpreted as an integer index -- its value in physical units
        depends entirely on the interval of time between the frames in your
        trajectory file''')
        
    a1 = argument('trajectories', nargs='+', help='''Path to one or more MD
        trajectory files or glob patterns that match MD trajectory files.''')
    a2 = argument('--out', default='tica-projection.h5', help='''The results
        will be saved to this path as a .h5 file using mdtraj.io.saveh().
        (default=pca-projection.h5)''')


    def __init__(self, args):
        from projector.models.tica import tICA
        if args.offset <= 0:
            self.error('offset must be greater than or equal to zero')
        self.args = args
        self.model = tICA(n_components=2, offset=self.args.offset)
        self.labels = ['tIC1', 'tIC2']

    # inherit start() from PCA