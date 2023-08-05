# nparray

**High-Level Wrappers for Building and Manipulating Numpy Arrays**

[![badge](https://img.shields.io/badge/github-kecnry%2Fnparray-blue.svg)](https://github.com/kecnry/nparray)
[![badge](https://img.shields.io/badge/pip-nparray-blue.svg)](https://pypi.org/project/nparray/)
[![badge](https://img.shields.io/badge/license-GPL3-blue.svg)](https://github.com/kecnry/nparray/blob/master/LICENSE)
[![badge](https://travis-ci.org/kecnry/nparray.svg?branch=master)](https://travis-ci.org/kecnry/nparray)
[![badge](https://readthedocs.org/projects/nparray/badge/?version=latest)](https://nparray.readthedocs.io/en/latest/?badge=latest)

Create numpy arrays (via arange, linspace, etc) and manipulate the creation arguments at any time.  The created object acts as a numpy array but only stores the input parameters until its value is accessed.

Read the [latest documentation on readthedocs](https://nparray.readthedocs.io) or [browse the current documentation](./docs/index.md).


## Dependencies

**nparray** requires the following dependencies:

  - python 2.7+ or 3.6+
  - numpy 1.10+
  - collections (should be standard python module)

and the following optional dependencies:

  - astropy 1.0+ (required for units support)

You can see the [Travis testing matrix](https://travis-ci.org/kecnry/nparray) for
details on what exact versions have been tested and ensured to work.  If you run
into any issues with dependencies, please [submit an issue](https://github.com/kecnry/nparray/issues/new).

## Installation

**nparray** is available via [pip](https://pypi.org/project/nparray/):

```sh
pip install nparray
```

Alternatively, to install from source, use the standard python setup.py commands.

To install globally:
```sh
python setup.py build
sudo python setup.py install
```

Or to install locally:
```sh
python setup.py build
python setup.py install --user
```

## Basic Usage

**nparray** is imported as a python module:

```
import nparray
```

Read the [latest documentation on readthedocs](https://nparray.readthedocs.io) or [browse the current documentation](./docs/index.md).

## Contributors

[Kyle Conroy](https://github.com/kecnry)

Contributions are welcome!  Feel free to file an issue or fork and create a pull-request.
