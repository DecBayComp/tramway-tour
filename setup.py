# -*- coding: utf-8 -*-

from setuptools import setup
from hashlib import md5
from urllib.request import urlretrieve
import tarfile
from os import path

setup(
    name = 'tramway-tour',
    version = '0.4.1',
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
    packages = [
        'src',
        'src.quick_example',
        'src.tracking',
        'src.segmentation',
        'src.inference',
        'src.data',
    ],
    package_data = {
        'src': ['data/*.tif', 'data/*.txt', 'data/*.rwa', 'notebooks/*.webm'],
        },
    #install_requires = ['tramway[full]'], # use requirements.txt
)

# get package data
package_data_filename = 'package_data.tar.bz2'
#package_data_download_link = 'http://dl.pasteur.fr/fop/jo7w4WPq/package_data.tar.bz2'
package_data_download_link = 'https://gitlab.pasteur.fr/flaurent/tramway-artefacts/-/raw/main/doc/package_data.tar.bz2?inline=false'
package_data_checksum = '7ef509c9691661e74f405d59cadcc3a1'

def download_and_extract():
    package_data_filepath = package_data_filename
    try:
        with open(package_data_filepath, 'rb') as f:
            actual_checksum = md5(f.read()).hexdigest()
        assert actual_checksum == package_data_checksum
    except Exception:
        urlretrieve(package_data_download_link, package_data_filepath)
        with tarfile.open(package_data_filepath) as f:
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(f, ".")
        return True
    else:
        return False

download_and_extract()

