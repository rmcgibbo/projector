import os
from sklearn import decomposition
import numpy as np
import json
from flask import Flask, url_for, render_template, redirect
app = Flask(__name__)

import mdtraj as md
TRAJ_FN = '/home/rmcgibbo/projects/met-enkephalin/output-1-dry.h5'
TOP_FN = '/home/rmcgibbo/projects/met-enkephalin/1PLX.pdb'
with open(TOP_FN) as f:
    TOP_PDB_TEXT = f.read()
TRAJECTORY = md.load(TRAJ_FN, top=TOP_FN)
TRAJECTORY.center_coordinates()
TRAJECTORY.superpose(TRAJECTORY, 0)

PREV_COORD = 0

#-----------------------------------------------------------------------------#

@app.route('/')
def index():
    return app.send_static_file('index.html')
@app.route('/GLmol/<path:path>')
def static1(path):
    return app.send_static_file(os.path.join('GLmol', path))
@app.route('/js/<path:path>')
def static2(path):
    return app.send_static_file(os.path.join('js', path))
@app.route('/css/<path:path>')
def static3(path):
    return app.send_static_file(os.path.join('css', path))

#-----------------------------------------------------------------------------#

@app.route('/points.json')
def points_json():
    phi = md.compute_phi(TRAJECTORY)[1] * (180 / np.pi)
    psi = md.compute_psi(TRAJECTORY)[1] * (180 / np.pi)
    data = np.hstack((phi, psi))

    pca = decomposition.PCA(n_components=2)
    xy = pca.fit_transform(data)
    
    
    return json.dumps({'x': xy[:,0].tolist(), 'y': xy[:,1].tolist()})

@app.route('/pdb')
def pdb():
    return TOP_PDB_TEXT

@app.route('/coordinates/<int:index>')
def coordinates(index):
    global PREV_COORD

    print index
    
    # nanometer to angstroms
    frame = TRAJECTORY[index]
    frame.superpose(TRAJECTORY, PREV_COORD)
    TRAJECTORY.xyz[index] = frame.xyz[0]


    xyz = frame.xyz * 10.0
    return json.dumps({
        'x': xyz[0, :, 0].tolist(),
        'y': xyz[0, :, 1].tolist(),
        'z': xyz[0, :, 2].tolist()
    })

    PREV_COORD = index


if __name__ == '__main__':
    app.run(debug=True)
