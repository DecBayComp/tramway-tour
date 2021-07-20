# Regions of interest

Once the localized or tracked data are loaded as a dataframe, regions of interest can be selected at particle density peaks, for example as square areas centered at these peak locations.

The `tramway.analyzer.roi.utils` module exports a simple `density_based_roi` function to do so, as an example. Its usage is better illustrated in [another notebook](https://mybinder.org/v2/gh/DecBayComp/TRamWAy/HEAD?filepath=notebooks%2FRWAnalyzer%20tour.ipynb#ROI-definition) (section *ROI definition*), part of the TRamWAy project.

The time support for each space ROI can also be restricted to a time segment with relatively sustained density.

TRamWAy does not encourage a specific approach, but the general rule is to select regions that contain enough data for the estimation techniques involved at the inference stage to work properly.

Considering coordinates named `'x'`, `'y'` (space), `'t'` (time), regions of interest can be defined as bounding boxes, in a dataframe with one row per ROI, and columns `'x min'`, `'x max'`, `'y min'`, `'y max'`, `'t min'`, `'t max'`, etc.


```python
import pandas as pd

my_single_roi = pd.DataFrame({'x min': [0], 'x max': [1], 'y min': [0], 'y max': [1]})
```

Such a dataframe can be passed to the `roi.from_bounding_boxes` function exported by the `tramway.analyzer` module, and the returned value be assigned to the `roi` attribute of an `SPTDataItem` object.


```python
from tramway.analyzer import *

a = RWAnalyzer()

a.spt_data = spt_data.from_ascii_files('../data/*_traj.rwa') # this actually matches a single file

for file in a.spt_data:
    file.roi = roi.from_bounding_boxes(my_single_roi)
```

Below is an example function to tighten the time support to the highest density series of contiguous time segments, for a given sliding time window. Data `df` are assumed to be cropped for a space ROI:


```python
import numpy as np

def time_support(df, dt, win_dur, win_shift, min_n_seg=5, absolute_min_n_transloc=20, triggering_min_n_transloc=50):
    """
    Define a contiguous time support for data `df`.
    
    Dataframe `df` should feature a column labelled :const:`'t'`.
    
    The resulting time support is adjusted for a sliding time window with duration `win_dur` and shift `win_shift`.
    Time segments are selected based on the number of associated rows in `df` (points).
    
    Time support selection operates in three steps:
    
    * the first and last time segments to exhibit `triggering_min_n_transloc` points are sought for, at frame interval (`dt`) resolution;
    * the sliding time window is applied to the overall time interval from such a segment to the other, so as to define a series of time segments;
      the series is split into possibly multiple "fragments", discarding the time segments with less than `absolute_min_n_transloc` points;
    * the longest fragment (or contiguous series of pre-selected time segments) is selected and the corresponding start and stop times are returned.
    
    If no such time segments can be found, or fewer than `min_n_seg`, :const:`None` is returned instead.
    """
    t = df['t'].values
    t0, t1 = t.min(), t.max()
    # redefine support [t0, t1] so that first and last segments satisfy triggering_min_n_transloc
    ts = np.arange(t0, t1+.5*dt, dt)
    cum_n = np.array([ np.sum((t_-win_dur-.5*dt<t)&(t<t_+.5*dt)) for t_ in ts ])
    ok = np.flatnonzero(triggering_min_n_transloc <= cum_n)
    if ok.size < 2:
        return None
    i, j = ok[0], ok[-1]
    t0, t1 = ts[i]-win_dur, ts[j]
    n_seg = np.round((t1 - t0 - win_dur) / win_shift) + 1
    if n_seg < min_n_seg:
        return None
    t_tot = (n_seg - 1) * win_shift + win_dur
    t_wasted = (t1 - t0) - t_tot
    if 0 < t_wasted:
        t0 += t_wasted / 2
        t1 -= t_wasted / 2
    # fragment the [t0, t1] support discarding the segments with less than absolute_min_n_transloc points
    seg_start = np.arange(t0, t1-win_dur+.5*dt, win_shift)
    seg = np.hstack((seg_start[:,None], seg_start[:,None]+win_dur))
    transloc_count = np.array([ np.sum((t0_-.5*dt<t)&(t<t1_+.5*dt)) for t0_, t1_ in seg ])
    ok = absolute_min_n_transloc <= transloc_count
    fragment_start = np.flatnonzero( np.r_[True, ~ok[:-1]] & ok )
    fragment_stop = np.flatnonzero( ok & np.r_[~ok[1:], True] )
    assert fragment_start.size == fragment_stop.size
    # select the longest fragment (= series of successive segments)
    fragment_len = fragment_stop - fragment_start
    longest_fragment = np.argmax(fragment_len)
    if fragment_len[longest_fragment] < min_n_seg:
        return None
    i, j = fragment_start[longest_fragment], fragment_stop[longest_fragment]
    t0, t1 = seg[i,0], seg[j,1]
    return t0, t1
```
