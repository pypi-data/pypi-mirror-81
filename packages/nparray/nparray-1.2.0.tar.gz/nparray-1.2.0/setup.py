#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nparray',
      version='1.2.0',
      description='High-Level Wrappers for Building and Manipulating Numpy Arrays',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Kyle Conroy',
      author_email='kyleconroy@gmail.com',
      url='https://www.github.com/kecnry/nparray',
      download_url = 'https://github.com/kecnry/nparray/tarball/1.2.0',
      packages=['nparray'],
      install_requires=['numpy>=1.10'],
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
       ],
     )
