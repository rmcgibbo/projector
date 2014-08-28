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
from mixtape.cmdline import argument, argument_group
from projector.pca import PCACommand

__all__ = ['tICACommand']


class tICACommand(PCACommand):
    name = 'tica'
    description = 'Compute 2D projection with time-structure independent components analyis (tICA)'

    g = argument_group('required arguments')
    g.add_argument('--featurizer', required=True, help='''Path to a featurizer
        pickle. These can be created with the 'hmsm featurizer' command in
        mixtape.''')
    g.add_argument('--lag-time', required=True, type=int, help='''Delay time
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
        from mixtape.tica import tICA
        if args.lag_time <= 0:
            self.error('offset must be greater than or equal to zero')
        self.args = args
        self.model = tICA(n_components=2, lag_time=self.args.lag_time)
        self.labels = ['tIC1', 'tIC2']

    # inherit start() from PCA
