# Scalability

While the inference stage is the most common computational bottleneck, localization microscopy data often come as multiple files of wide-field images that exhibit the fluorescent biomolecule spatially distributed as spots that can be selectively targeted as [regions of interest](roi.ipynb) for analysis.

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
* `SingularitySlurm`: jobs are submitted on a remote <abbr title="High Performance Computing">HPC</abbr> cluster enabled with the Slurm workload manager, with support for Singularity containers

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
