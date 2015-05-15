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
import os
import json
import pickle
import tempfile
import six
import operator
from itertools import groupby
from six.moves import zip

import numpy as np
from flask import Flask, request

import mdtraj as md
from msmbuilder.cmdline import Command, argument, FlagAction

CHAIN_NAMES = [chr(ord('A') + i) for i in range(26)]

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------


class PlotCommand(Command, Flask):
    name = 'plot'
    _group = 1
    _concrete = True
    description = 'Launch the interactive plot of a projection in the browser.'
    a1 = argument('projection-file')
    a2 = argument('--n-bins', type=int, default=50)
    a3 = argument('--debug', action=FlagAction, default=False)
    a4 = argument('--progressive', action=FlagAction, default=False)

    def __init__(self, args):
        import pylru
        from mdtraj import io
        from scipy.spatial import cKDTree

        self.args = args
        self.data = io.loadh(args.__dict__['projection-file'], deferred=False)
        self.kdtree = cKDTree(self.data['X'])

        self.top = pickle.loads(self.data['topology'][0])
        self.top.center_coordinates()
        self.topology_pdb_sring = pdb_string(self.top)
        self.alpha_carbon_indices = np.array(
            [a.index for a in self.top.top.atoms if a.name == 'CA'])

        self._traj_cache = pylru.lrucache(size=100)
        self._last_index = 0

        static_folder = os.path.join(os.path.dirname(__file__), 'static')
        s = super(PlotCommand, self) if six.PY2 else super()
        s.__init__(__name__, static_folder=static_folder)

    def start(self):

        self.add_url_rule('/', 'handle_index', self.handle_index)
        self.add_url_rule('/js/<path:path>', 'handle_js', self.handle_js)
        self.add_url_rule('/css/<path:path>', 'handle_css', self.handle_css)

        self.add_url_rule('/pdb', 'handle_pdb', self.handle_pdb)
        self.add_url_rule('/heatmap.json', 'handle_heatmap_json', self.handle_heatmap_json)
        self.add_url_rule('/xy', 'handle_xy', self.handle_xy)

        self.handle_heatmap_json()
        print('\n', '=' * 20, 'OPEN YOUR BROWSER TO SEE THE PLOT', '=' * 20)
        self.run(debug=self.args.debug)

    def load_frame(self, filename, index):
        import mdtraj as md

        if filename not in self._traj_cache:
            print('loading %s...' % filename)
            kwargs = {} if os.path.splitext(
                filename)[1] in {'.h5', '.lh5', '.pdb'} else {'top': self.top}
            self._traj_cache[filename] = md.load(filename, **kwargs)
            self._traj_cache[filename].center_coordinates()

            print('...done loading')

        return self._traj_cache[filename][index]

    def compute_secondary(self, frame):
        dssp = md.compute_dssp(frame, simplified=True)[0]
        helices, sheets = [], []

        for k, g in groupby(enumerate(dssp), operator.itemgetter(1)):
            indices, keys = list(zip(*g))
            start_residue = indices[0]
            end_residue = indices[-1]
            run = [CHAIN_NAMES[self.top.topology.residue(start_residue).chain.index],
                   start_residue,
                   CHAIN_NAMES[self.top.topology.residue(end_residue).chain.index],
                   end_residue]
            if k == 'H':
                helices.append(run)
            elif k == 'E':
                sheets.append(run)
        return helices, sheets

    # -------------------------------------------------------------------------#

    def handle_index(self):
        return self.send_static_file('index.html')

    def handle_js(self, path):
        return self.send_static_file(os.path.join('js', path))

    def handle_css(self, path):
        return self.send_static_file(os.path.join('css', path))

    def handle_pdb(self):
        helices, sheets = self.compute_secondary(self.top)
        return json.dumps({
            'pdbstring': self.topology_pdb_sring,
            'helices': helices,
            'sheets': sheets})

    def handle_heatmap_json(self):
        x = self.data['X'][:, 0]
        y = self.data['X'][:, 1]

        heatmap, xedges, yedges = np.histogram2d(x, -y, bins=self.args.n_bins)

        return json.dumps({
            'heatmap': heatmap.T.tolist(),
            'vmax': float(np.max(heatmap)),
            'extent': {'xmin': xedges[0], 'xmax': xedges[-1],
                       'ymin': -yedges[-1], 'ymax': -yedges[0]}
        })

    def handle_xy(self):
        x = float(request.args.get('x', 0))
        y = float(request.args.get('y', 0))

        _, index = self.kdtree.query(x=[x, y], k=1)

        frame = self.load_frame(
            self.data['fns'][index].decode('utf-8'),
            self.data['indices'][index])

        if self.args.progressive:
            oldframe = self.load_frame(
                self.data['fns'][self._last_index],
                self.data['indices'][self._last_index])
            superpose_target = oldframe
            self._last_index = index
        else:
            superpose_target = self.top

        frame.superpose(superpose_target, atom_indices=self.alpha_carbon_indices)
        helices, sheets = self.compute_secondary(frame)
        # convert to angstroms
        xyz = frame.xyz[0] * 10.0

        return json.dumps({
            'x': xyz[:, 0].tolist(),
            'y': xyz[:, 1].tolist(),
            'z': xyz[:, 2].tolist(),
            'helices': helices,
            'sheets': sheets,
        })


def pdb_string(trajectory, frame=0):
    try:
        fd, fn = tempfile.mkstemp('.pdb')
        os.close(fd)
        conf = trajectory[frame]
        conf.center_coordinates()
        conf.save(fn)
        with open(fn) as f:
            return f.read()
    finally:
        os.unlink(fn)
