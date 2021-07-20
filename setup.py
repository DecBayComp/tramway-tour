# -*- coding: utf-8 -*-

from setuptools import setup
from hashlib import md5
from urllib.request import urlretrieve
import tarfile
from os import path

setup(
    name = 'tramway-tour',
    version = '0.4',
    description = 'Notebook-based documentation for TRamWAy',
    url = 'https://github.com/DecBayComp/tramway-tour',
    author = 'Institut Pasteur, François Laurent',
    author_email = 'francois.laurent@pasteur.fr',
    license = 'Zero-Clause BSD',
    classifiers = [
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    packages = ['src'],
    package_data = {
        'src': ['data/*.tif', 'data/*.txt', 'data/*.rwa', 'notebooks/*.webm'],
        },
)

# get package data
package_data_filename = 'package_data.tar.bz2'
package_data_download_link = 'http://dl.pasteur.fr/fop/jo7w4WPq/package_data.tar.bz2'
package_data_checksum = 'dddf23009687559fbe912ad8a3515b4c'

def download_and_extract():
    package_data_filepath = package_data_filename
    try:
        with open(package_data_filepath, 'rb') as f:
            actual_checksum = md5(f.read()).hexdigest()
        assert actual_checksum == package_data_checksum
    except Exception:
        urlretrieve(package_data_download_link, package_data_filepath)
        with tarfile.open(package_data_filepath) as f:
            f.extractall('.')
        return True
    else:
        return False

download_and_extract()

