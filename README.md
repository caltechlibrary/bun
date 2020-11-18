Quiche<img width="11%" align="right" src="https://raw.githubusercontent.com/caltechlibrary/quiche/main/.graphics/quiche-logo.png">
======

Quiche (_**Q**uintessential **UI** **C**lass **H**i**E**rarchy_) is a small Python package for very basic user interactions.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square)](https://choosealicense.com/licenses/bsd-3-clause)
[![Latest release](https://img.shields.io/github/v/release/caltechlibrary/template.svg?style=flat-square&color=b44e88)](https://github.com/caltechlibrary/template/releases)


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

This package grew out of a desire to satisfy two goals simultaneously: (1) have the simplest possible coding interface for printing informational messages and getting basic information from the user; and (2) let the user choose to use a command-line interface (CLI) or a graphical user interface (GUI) at run time.  Quiche (_**Q**uintessential **UI** **C**lass **H**i**E**rarchy_) is the result.  It provides functions such as `inform`, `warn`, `alert` and others, which you can use in code such as

```python
if not writable(dest_dir):
    alert(f'Cannot write output in {dest_dir}.')
    return
if not results:
    warn(f'Nothing to do for {item}')
    return
```

By necessity, Quiche is simple and limited in functionality, as well as being somewhat opinionated in its approach, but it satisfies the needs of many programs.  Many user interface packages already exist for Python, but their use requires configuration and more complicated code to use.  Quiche wraps packages such as [Rich](https://rich.readthedocs.io/en/latest/) and [wxPython](https://wxpython.org) to provide simple high-level calls.


Installation
------------

The instructions below assume you have a Python interpreter installed on your computer; if that's not the case, please first [install Python version 3](INSTALL-Python3.md) and familiarize yourself with running Python programs on your system.

On **Linux**, **macOS**, and **Windows** operating systems, you should be able to install `quiche` with [`pip`](https://pip.pypa.io/en/stable/installing/).  To install `quiche` from the [Python package repository (PyPI)](https://pypi.org), run the following command:
```
python3 -m pip install quiche
```

As an alternative to getting it from [PyPI](https://pypi.org), you can use `pip` to install `quiche` directly from GitHub, like this:
```sh
python3 -m pip install git+https://github.com/caltechlibrary/quiche.git
```
 

Usage
-----

[_... forthcoming ..._]


Known issues and limitations
----------------------------

[_... forthcoming ..._]


Getting help
------------

If you find an issue, please submit it in [the GitHub issue tracker](https://github.com/caltechlibrary/quiche/issues) for this repository.


Contributing
------------

We would be happy to receive your help and participation with enhancing Quiche!  Please visit the [guidelines for contributing](CONTRIBUTING.md) for some tips on getting started.


License
-------

Software produced by the Caltech Library is Copyright (C) 2020, Caltech.  This software is freely distributed under a BSD/MIT type license.  Please see the [LICENSE](LICENSE) file for more information.


Authors and history
---------------------------

I developed the first version of this code while implementing [Holdit](https://github.com/caltechlibrary/holdit).  I started using the code in essentially every Python software package I have written since then, first by copy-pasting the code (which was initially very short) and eventually creating a single-file module (named `ui.py`).  This was obviously a suboptimal approach.  Finally, in 2020, I decided it was time to break it out into a proper self-contained Python package.


Acknowledgments
---------------

This work was funded by the California Institute of Technology Library.

<div align="center">
  <br>
  <a href="https://www.caltech.edu">
    <img width="100" height="100" src="https://raw.githubusercontent.com/caltechlibrary/quiche/main/.graphics/caltech-round.png">
  </a>
</div>
