Bun<img width="11%" align="right" src="https://github.com/caltechlibrary/bun/raw/main/.graphics/bun-icon.png">
===========================================================================

Bun (_**B**asic **U**ser I**n**terface_) is a small Python package for a basic user interface.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/bun.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/bun/releases)
[![Python](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat-square)](http://shields.io)
[![DOI](https://img.shields.io/badge/dynamic/json.svg?label=DOI&style=flat-square&color=lightgray&query=$.metadata.doi&uri=https://data.caltech.edu/api/record/1679)](https://data.caltech.edu/records/1679)
[![PyPI](https://img.shields.io/pypi/v/bun.svg?style=flat-square&color=orange)](https://pypi.org/project/bun/)

Table of contents
-----------------

* [Introduction](#introduction)
* [Installation](#installation)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Authors and history](#authors-and-history)
* [Acknowledgments](#authors-and-acknowledgments)


Introduction
------------

This package grew out of a desire to satisfy two goals simultaneously: (1) have the simplest possible coding interface for printing color-coded messages and getting basic information from the user; and (2) let the user choose to use a command-line interface (CLI) or a graphical user interface (GUI) at run time.  Bun (_**B**asic **U**ser I**n**terface_) is the result.  It provides functions such as `inform`, `warn`, `alert` and others, which you can use in code like this:

```python
if writable(dest_dir):
    inform(f'Will write output to {dest_dir}.')
else:
    alert(f'Output destination {dest_dir} is not writable.')
```

Bun is simple and limited in functionality, as well as being somewhat opinionated in its design, but it satisfies the needs of many programs.  Bun wraps packages such as [Rich](https://rich.readthedocs.io/en/latest/) and [wxPython](https://wxpython.org) to provide simple high-level calls.  Here is some sample output from an application that uses Bun:

<p align="center">
<img src="https://github.com/caltechlibrary/bun/raw/main/.graphics/cli-output-example.png">
</p>

Many user interface packages already exist for Python, but their use requires configuration and more complicated code to use.  Bun aims to be simpler. 


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `bun` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `bun` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install bun
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `bun` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/bun.git
```
 

Usage
-----

[_... forthcoming ..._]


Known issues and limitations
----------------------------

[_... forthcoming ..._]


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/bun/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing Bun!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2020, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

I developed the first version of this code while implementing [Holdit](https://github.com/caltechlibrary/holdit).  I started using the code in essentially every Python software package I have written since then, first by copy-pasting the code (which was initially very short) and eventually creating a single-file module (named `ui.py`).  This was obviously a suboptimal approach.  Finally, in 2020, I decided it was time to break it out into a proper self-contained Python package.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

The [vector artwork](https://thenounproject.com/term/bun/1979298/) of a bun, used as the icon for this repository, was created by [Vectors Market](https://thenounproject.com/vectorsmarket/) from the Noun Project.  It is licensed under the Creative Commons [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/) license.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/bun/main/.graphics/caltech-round.png">
  </a>
</div>
