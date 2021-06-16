
import tarfile
from pathlib import Path
project_dir = Path(__file__).resolve().parents[2]

def make_dataset():
    pass

package_data_files = [
        'data/demo1.txt',
        'data/Image_8bit.tif',
        'data/Image_loc.txt',
        'data/Image_traj.txt',
        'data/Image_traj-roi.txt',
        'data/Image_traj.rwa',
        'notebooks/locations_only.webm',
        'notebooks/trajectories.webm',
        ]
package_data_filename = 'package_data.tar.bz2'

def package_data():
    with tarfile.open(project_dir / package_data_filename, mode='w:bz2') as f:
        for filepath in package_data_files:
            f.add(str(project_dir / filepath), arcname=filepath)

