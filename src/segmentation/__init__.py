from tramway.analyzer import *
import numpy as np

from ..data import project_dir

datafile = project_dir / 'data/demo1.txt'

def preset_analyzer(return_translocations=False):
    np.random.seed(123456789)
    a = RWAnalyzer()
    a.spt_data = spt_data.from_ascii_file(str(datafile))
    a.spt_data.frame_interval = .04 # in s
    a.spt_data.localization_precision = .02 # in µm
    if return_translocations:
        translocations = a.spt_data.dataframe
        return a, translocations
    else:
        return a
    
def preset_analyzers(n=2):
    a, translocations = preset_analyzer(True)
    analyzers = [a]
    for _ in range(1, n):
        analyzers.append(preset_analyzer())
    output_args = tuple(analyzers) + (translocations,)
    return output_args

def set_notebook_theme():
    return
    import matplotlib as mpl
    clr = 'white'
    mpl.rcParams['axes.titlecolor'] = clr
    mpl.rcParams['axes.labelcolor'] = clr
    mpl.rcParams['xtick.color'] = clr
    mpl.rcParams['ytick.color'] = clr

