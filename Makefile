
datafiles= \
	   data/demo1.txt \
	   data/Image_loc.txt \
	   data/Image_traj.txt \
	   data/Image_traj-roi.txt \
	   data/Image_traj.rwa
excluded_data_files= \
		     data/Image_8bit.tif
extrafiles= \
	    notebooks/locations_only.webm \
	    notebooks/trajectories.webm
docfiles= \
	  docs/locations_only.webm \
	  docs/trajectories.webm \
	  $(wildcard docs/tracking_files/tracking_*_*.png) \
	  $(wildcard docs/segmentation_files/segmentation_*_*.png) \
	  $(wildcard docs/inference_files/inference_*_*.png)
package_data_file= package_data.tar.bz2

files_to_transfer=$(patsubst notebooks/%,docs/%,$(extrafiles))
notebooks=$(wildcard notebooks/*.ipynb)
md_pages=$(patsubst notebooks/%.ipynb,docs/%.md,$(notebooks))
patches=$(wildcard docs/*.patch)
files_to_patch=$(patches:.patch=)


env:
	mkvirtualenv -r requirements-mkdocs.txt tramway-mkdocs

pages: $(md_pages) $(patches)
#	for target in $(files_to_patch); do patch -Nr- "$(target)" "$(target).patch"; done

docs/%.md: notebooks/%.ipynb
	jupyter nbconvert\
		--to markdown $<\
		--output-dir $(dir $@) &&\
	rm -rf docs/*-*

data: $(datafiles) $(extrafiles) $(docfiles)
	rm -f $(package_data_file) &&\
	       	tar jcvf $(package_data_file) $^

clean:
	rm -rf docs/*.md docs/*_files/

