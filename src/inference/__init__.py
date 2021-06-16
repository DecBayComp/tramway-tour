from tramway.analyzer import *
import numpy as np
import pandas as pd

from ..data import project_dir

datafile = project_dir / 'data/Image_traj.txt'

def reset_data():
    import os
    rwa_file = os.path.splitext(str(datafile))[0]+'.rwa'
    try:
        os.unlink(rwa_file)
    except FileNotFoundError:
        pass

def preset_analyzer():
    a = RWAnalyzer()

    a.spt_data.from_ascii_file(datafile)
    a.spt_data.frame_interval = .04 # in s
    a.spt_data.localization_precision = .02 # in µm

    # bounding box for space coordinates (x, y)
    center = [17.3619, 19.2112]
    side = 2.5
    # bounding box for time
    t0, t1 = 180., 480.

    bb = pd.DataFrame({
        'x min': center[0] - .5 * side,
        'x max': center[0] + .5 * side,
        'y min': center[1] - .5 * side,
        'y max': center[1] + .5 * side,
        't min': t0,
        't max': t1,
        }, index=[0])
    a.roi.from_bounding_boxes(bb)

    r = single(a.roi)
    translocations = r.crop()
    translocations = r.discard_static_trajectories(translocations)

    a.tesseller = tessellers.KMeans
    a.tesseller.resolution = .05

    a.sampler = sampler.Knn(10)

    assignment = a.sampler.sample(translocations)

    return a, assignment

def set_notebook_theme():
    return
    import matplotlib as mpl
    clr = 'white'
    mpl.rcParams['text.color'] = clr
    mpl.rcParams['axes.titlecolor'] = clr
    mpl.rcParams['axes.labelcolor'] = clr
    mpl.rcParams['xtick.color'] = clr
    mpl.rcParams['ytick.color'] = clr

