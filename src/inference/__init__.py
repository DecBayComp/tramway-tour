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

def set_notebook_theme(theme='light'):
    if theme == 'dark':
        import matplotlib as mpl
        clr = 'white'
        mpl.rcParams['text.color'] = clr
        mpl.rcParams['axes.titlecolor'] = clr
        mpl.rcParams['axes.labelcolor'] = clr
        mpl.rcParams['xtick.color'] = clr
        mpl.rcParams['ytick.color'] = clr

def reload_movies():
    dv_t = RWAnalyzer()

    dv_t.spt_data.from_rwa_file('../data/Image_traj.rwa')
    dv_t.spt_data.frame_interval = .04  # in s
    dv_t.spt_data.localization_precision = .02  # in µm

    dv_t.roi.from_ascii_files() # default filepath will be '../data/Image_traj-roi.txt'

    dv_t.tesseller = tessellers.KMeans
    dv_t.tesseller.resolution = .1  # in µm

    dv_t.time = time.SlidingWindow(duration=60, shift=30)

    dv_t.sampler = sampler.Knn(10)

    dv_t.mapper = models.DV(start='stochastic')

    sampling_label = lambda roi_label: roi_label + ' - kmeans + 60s window'
    map_label = 'dv maps'

    r = single(dv_t.roi)
    assignment_t = r.get_sampling(sampling_label)
    dv_t_maps = assignment_t.get_child(map_label)

    return dv_t_maps
