from tramway.analyzer import *
from ..data import project_dir

def example_trajectory_movie_file():
    print('playback rate is 0.2')
    return 'trajectories.webm'

def example_dv_maps(overlay_particle_locations=False, axes=None):
    a = RWAnalyzer()
    a.spt_data.from_rwa_file(project_dir / 'data/Image_traj.rwa')
    a.roi.from_ascii_files()
    #a.tesseller = tessellers.KMeans
    #a.tesseller.resolution = .1
    a.time = time.SlidingWindow(duration=60, shift=30)
    #a.sampler = sampler.Knn(10)
    #a.mapper = mapper.MapperPlugin('stochastic.dv')
    #a.mapper.potential_prior = 606.5625
    #a.mapper.potential_prior = 0.252734375
    #a.mapper.time_prior = 1.
    #a.mapper.verbose = False
    sampling_label = lambda roi_label: roi_label + ' - kmeans + 60s window'
    map_label = 'dv maps'
    #
    if overlay_particle_locations is True:
        overlay_particle_locations = {'markersize': 2}
    #
    r = single(a.roi)
    assignment = r.get_sampling(sampling_label)
    maps = assignment.get_child(map_label)
    if axes is None:
        from matplotlib import pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(16,6))
    movie = a.mapper.mpl.animate(fig, maps,
            feature='diffusivity',
            axes=axes[0], unit='std',
            overlay_locations=overlay_particle_locations)
    movie = a.mapper.mpl.animate(movie, maps,
            feature='potential',
            axes=axes[1], unit='std',
            overlay_locations=overlay_particle_locations)
    #
    return movie

