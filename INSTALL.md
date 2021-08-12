
``
git clone https://github.com/DecBayComp/tramway-tour
cd tramway-tour
mkvirtualenv tramway-mkdocs
pip install -e .
pip install mkdocs mkdocs-material

# optional, to use the master branch of TRamWAy instead of the latest release
pip install -e ../TRamWAy/[hpc,webui]

pip install ipykernel
python -m ipykernel install --user --name=tramway-mkdocs   # --user still required
``

