
datafiles= \
	   data/demo1.txt \
	   data/Image_8bit.tif \
	   data/Image_loc.txt \
	   data/Image_traj.txt \
	   data/Image_traj-roi.txt \
	   data/Image_traj.rwa
extrafiles= \
	    notebooks/locations_only.webm \
	    notebooks/trajectories.webm
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
		--output-dir $(dir $@)

data: $(datafiles) $(localfiles)
	rm -f $(package_data_file) &&\
	       	tar jcvf $(package_data_file) $^

clean:
	rm -f docs/*.md

