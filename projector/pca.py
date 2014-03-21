# Author: Robert McGibbon <rmcgibbo@gmail.com>
# Contributors:
# Copyright (c) 2014, Stanford University
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import print_function, division, absolute_import
from mixtape.featurizer import featurize_all
from mixtape.cmdline import Command, argument, argument_group


class PCACommand(Command):
    name = 'pca'
    description = 'compute a projection with principle components analysis (PCA).'

    g = argument_group('required argument')
    g.add_argument('--featurizer', required=True, help='''Path to a featurizer
        pickle. These can be created with the 'hmsm featurizer' command in
        mixtape.''')
    a1 = argument('trajectories', nargs='+', help='''Path to one or more MD
        trajectory files or glob patterns that match MD trajectory files.''')
    a2 = argument('--out', default='pca-projection.h5', help='''The results
        will be saved to this path as a .h5 file using mdtraj.io.saveh().
        (default=pca-projection.h5)''')

    def __init__(self, args):
        self.args = args

    def start(self):
        import pickle
        from mdtraj import io
        from glob import glob
        import numpy as np
        from sklearn.decomposition import PCA

        featurizer = np.load(self.args.featurizer)
        topology = featurizer.reference_traj
        filenames = [fn for t in self.args.trajectories for fn in glob(t)]

        X, indices, fns = featurize_all(filenames, featurizer, topology)
        y = PCA(n_components=2).fit_transform(X)
        labels = np.array(['PC1', 'PC2'])

        io.saveh(self.args.out, X=y, indices=indices, fns=fns, labels=labels,
                 featurizer=np.array([pickle.dumps(featurizer)]))
        print('PCA projection saved: %s' % self.args.out)
