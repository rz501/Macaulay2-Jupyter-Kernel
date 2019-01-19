# M2JK - Jupyter kernel for Macaulay2

[![](https://img.shields.io/travis/radoslavraynov/Macaulay2-Jupyter-Kernel.svg?style=flat-square)](https://travis-ci.org/radoslavraynov/Macaulay2-Jupyter-Kernel)
[![](https://img.shields.io/pypi/v/macaulay2-jupyter-kernel.svg?style=flat-square)](#link-to-pypi-page)
<!-- [![](https://img.shields.io/badge/version-0.2.0-blue.svg?style=flat-square)](#) -->

## WORK IN PROGRESS - DON'T USE UNTIL THE RELEASE

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).

M2JK is intended as a drop-in replacement for Emacs, so after installing it,
you can fire up Jupyter and start coding right away.
Some of the features that come with it are
organizing your code into logical blocks (cells),
using alternative (non-Emacs) key bindings,
using Markdown and TeX inline,
storing and sharing your Macaulay2 code and output in a convenient way,
and easily exporting to `m2`, `ipynb`, `html`, `pdf` and other file formats.

The M2JK-specific features and configuration are [documented]() in the form of a Jupyter notebook.
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

![](/demo/screenshot.png?raw=true)

## Examples

* [features documentation](https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/features.ipynb)
* [screenshot demo](https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/minimal.ipynb) (the notebook in the screenshot)
* [preface to the Macaulay2 book](https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/p1m2book.ipynb)

Note that while the files above are statically rendered locally and reside on Github,
they are displayed thru [nbviewer](#) since Github seems to only support plain text output.
In particular, client-side syntax highlighting, such as in the screenshot,
is missing completely.

## Installation

### Prerequisites

Jupyter runs on Python. Recent versions of either Python 2 or Python 3 are OK.
Jupyter is then installed as a regular package, e.g. `pip3 install jupyter`.
For details, see its documentation online.
M2JK is written on Python 3.7 but distributed both as source and build,
so if installed from PyPI, you can do it with Python 2 too.

Macaulay2 needs to be installed and on your path.
If you are using Emacs as your front-end, it already is, but you can test it by `which M2`.
Otherwise, you can achieve that by running `setup()` from within an M2 session.
Alternatively, you can configure M2JK to use a specific binary.

### Install

You can install the latest stable version directly from PyPI by

```bash
$ pip3 install macaulay2-jupyter-kernel
$ python3 -m m2_kernel.install
```

Alternatively, you can install the latest development version from source by

```bash
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel.git
$ pip3 install macaulay2-jupyter-kernel/  # keep the forward slash or cd into the directory 
$ python3 -m m2_kernel.install
```

### Run on Jupyter

Once the installation is complete, you need to start (or restart) Jupyter by

```bash
$ jupyter notebook &
```

This shoud fire up a browser for you. If not, copy the output URL into one.
Then select File ⇨ New Notebook ⇨ M2 from the main menu.

## License

This software is not part of Macaulay2 and is released under the MIT License.
