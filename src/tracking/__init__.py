from ..data import project_dir

def set_notebook_theme(theme='light'):
    if theme == 'dark':
        import matplotlib as mpl
        clr = 'white'
        mpl.rcParams['text.color'] = clr
        mpl.rcParams['axes.labelcolor'] = clr
        mpl.rcParams['xtick.color'] = clr
        mpl.rcParams['ytick.color'] = clr

local_tif_file = project_dir / 'data/Image_8bit.tif'
tif_file_url = 'http://dl.pasteur.fr/fop/E9bLwkZ5/Image_8bit.tif'

def get_tif_file():
    import os
    from urllib.request import urlretrieve
    if not local_tif_file.exists():
        os.makedirs(os.path.dirname(local_tif_file), exist_ok=True) # for BinderHub env.
        urlretrieve(tif_file_url, str(local_tif_file))

