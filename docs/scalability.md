# Scalability

While the inference stage is the most common computational bottleneck, localization microscopy data often come as multiple files of wide-field images that exhibit the fluorescent biomolecule spatially distributed as spots that can be selectively targeted as [regions of interest](roi.md) for analysis.

TRamWAy features a few building blocks to conveniently implement the segmentation and inference stages, and optionally move the corresponding computations onto a remote high-performace computing (HPC) cluster.

## Building blocks

The `RWAnalyzer` object features a `pipeline` attribute that admits pipeline *stages*.
Several preset stages can be found in the `stages` module, such as `tessellate_and_infer` featured [elsewhere](inference.md#segmenting-and-inferring-all-at-once).

These preset stages are designed to handle multiple <abbr title="Single Particle Tracking">SPT</abbr> data files and regions of interest, and save to files. They perform their respective tasks so as to maximize the compatilibity between local and remote execution environments.
Basically, they are designed to run equally on the local host or a Slurm-enabled remote submit node.

This functionality is demonstrated in other notebooks ([1](https://mybinder.org/v2/gh/DecBayComp/TRamWAy/HEAD?filepath=notebooks%2FRWAnalyzer%20simple%20pipeline.ipynb) & [2](https://mybinder.org/v2/gh/DecBayComp/TRamWAy/HEAD?filepath=notebooks%2FRWAnalyzer%20multi-stage%20pipeline.ipynb)), part of the TRamWAy project.

## Environments

The `RWAnalyzer` object features an `env` attribute that can be left unset to make the `run` command locally execute the pipeline stage(s) and sequentially process the files/<abbr title="Regions Of Interest">ROI</abbr>.

Several preset environments can be used instead, to distribute the computations and maximize resource usage:

* `LocalHost`: multiprocessing on the local host
* `SingularitySlurm`: jobs are submitted on a remote <abbr title="High Performance Computing">HPC</abbr> cluster enabled with the [Slurm workload manager](https://slurm.schedmd.com/), with support for [Singularity](https://sylabs.io/guides/latest/user-guide/) containers

Again, this is better explained in [another notebook](https://mybinder.org/v2/gh/DecBayComp/TRamWAy/HEAD?filepath=notebooks%2FRWAnalyzer%20simple%20pipeline.ipynb).

### Making new `SingularitySlurm` adapters

As is, the `SingularitySlurm` environment does not point to the proper hostname and *scratch* location. Some operational environments are provided only for clusters that are internal to Institut Pasteur.

As an example, let us rewrite the `Maestro` environment (exported by the `environments` module), that corresponds to the Maestro <abbr title="High Performance Computing">HPC</abbr> cluster at Institut Pasteur:


```python
from tramway.analyzer.env.environments import SingularitySlurm
import os.path

class Maestro(SingularitySlurm):
    
    """
    The required hostname and scratch information must be provided as class
    methods.
    """
    
    @classmethod
    def hostname(cls):
        return 'maestro.pasteur.fr'
    
    @classmethod
    def scratch(cls, username):
        """
        This method returns the absolute path to the specified user's scratch
        directory.
        
        If no such dedicated directory exists, `scratch` can point to any
        directory in the user's $HOME instead, for example.
        """
        return os.path.join('/pasteur/sonic/scratch/users', username)
    
    """
    By default, the following command is executed on the submit host:
    
        singularity exec -H $HOME {default_container} python3.6 -s $@
        
    On some systems, additional options should be passed to Singularity.
    This can be done with the `singularity_options` class method:
    """
    
    @classmethod
    def singularity_options(cls):
        return '-B /pasteur'
    
    """
    Last but not least, Singularity may not be immediately available on the
    submit host. In the case of the Maestro server, Singularity comes as a
    *module* to be manually loaded.
    
    Generally speaking, any shell command to be run prior to calling
    Singularity can be specified in the `remote_dependencies` class method as a
    one-liner:
    """
    
    @classmethod
    def remote_dependencies(cls):
        return 'module load singularity'
        
```

### User-defined inference functions

In the case of user-defined functions passed to the `mapper` attribute as callable plugins, if these functions require extra dependencies that cannot be found in the default TRamWAy Singularity container, the `SingularitySlurm` environment (specifically) may crash unless provided with a properly augmented container.

A recipe can be found at [github.com/DecBayComp/TRamWAy/../containers/tramway-hpc-py36](https://github.com/DecBayComp/TRamWAy/blob/master/containers/tramway-hpc-py36).

* edit the recipe to include the additional dependencies (see also [github.com/DecBayComp/TRamWAy/../containers/available_images.rst](https://github.com/DecBayComp/TRamWAy/blob/master/containers/available_images.rst) for a list of included Python packages),
* build a container with the `singularity build` command, *e.g.*:
    ``singularity build --fakeroot my_container.sif my_recipe``
* copy the container file onto the remote host, preferably at your `$HOME` root directory,
* specify which container to use in your Python script:


```python
from tramway.analyzer import *

a = RWAnalyzer()

# ...

# import libraries for my_func

def my_func(*args):
    pass

a.mapper = mapper.MapperPlugin(my_func)

a.env = environments.Maestro # or any other SingularitySlurm specialization
# a.env.script = 'scalability.ipynb' # passing the current notebook's name is required from an IPython notebook
a.env.container = 'my_container.sif' # path relative to your $HOME directory on the remote host
```

### Standard containers

Standard Singularity image files (*.sif*) are named `tramway-hpc-YYMMDD-pyVV.sif`, with `YYMMDD` reflecting the date the file was generated, and ``VV`` the major and minor version numbers of Python.

These files are shared for a limited time using a big file sharing service at [dl.pasteur.fr](http://dl.pasteur.fr), and manually listed in the global dictionnary `tramway.analyzer.env.containers.singularity_containers`.

As a consequence, anyone may upload a container image file so that it can be downloaded from a designated url, and append the filename and corresponding url to the dictionnary, as an alternative to manually transferring the file onto remote worker hosts.

Note that containers are to be registered with the local instance of TRamWAy only. On remote workers, every TRamWAy instance already runs within such a container and should not try to call any container or even carry out introspection about the container it lives in.

To ensure better portability, developers are advised to select the container based on the oldest supported version of Python (*python3.6*), for example with:


```python
a.env.container = a.env.default_container(python_version='36')
```
