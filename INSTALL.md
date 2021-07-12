
``
git clone https://github.com/DecBayComp/tramway-tour
cd tramway-tour
mkvirtualenv tramway-mkdocs
pip install -e .

# optional, to use the master branch of TRamWAy instead of the latest release
pip install -e ../TRamWAy/[animate,roi,webui]

python -m ipykernel install --user --name=tramway-mkdocs
``

