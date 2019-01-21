# M2JK - Jupyter kernel for Macaulay2

[![](https://img.shields.io/travis/radoslavraynov/Macaulay2-Jupyter-Kernel.svg?style=flat-square)](https://travis-ci.org/radoslavraynov/Macaulay2-Jupyter-Kernel)
[![](https://img.shields.io/pypi/v/macaulay2-jupyter-kernel.svg?style=flat-square)](#link-to-pypi-page)
<!-- [![](https://img.shields.io/badge/version-0.2.0-blue.svg?style=flat-square)](#) -->

## WORK IN PROGRESS - DON'T USE UNTIL THE RELEASE

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).

M2JK is intended as a drop-in replacement for Emacs.
Some of the features that come with it are
organizing your code into logical blocks (cells),
alternative key bindings,
using Markdown and TeX in-line,
conveniently separating, storing and sharing your Macaulay2 code and output,
and exporting to various file formats like `m2`, `ipynb`, `html`, `pdf`, etc.
A small set of "cell magic" expressions configure kernel-specific options
like output mode, execution timeout and M2-executable path.

The M2JK-specific features and configuration are [documented]() as a Jupyter notebook.
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

## Screenshots

* [Screenshot 1](/demo/screenshot.png?raw=true)
* [Screenshot 2](/demo/screenshot.png?raw=true)

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

You need a recent version of Python and `pip`. Python 3 is recommended.
You can install Jupyter directly from PyPI.
```bash
pip3 install --upgrade pip
pip3 install jupyter
```

Macaulay2 needs to be installed and on your path.
If you are using Emacs as your front-end, it already is, but you can test it by `which M2`.
Otherwise, you can achieve that by running `setup()` from within an M2 session.
Alternatively, you can configure M2JK to use a specific binary.

### Install

You can install the latest release version directly from PyPI by

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

## Caveats

The current implementation is based on regular expressions matching in the Python runtime,
so there is considerable overhead with I/O-heavy programs.
Ideally, this issue will be addressed in the next (major) version.

## License

This software is not part of Macaulay2 and is released under the MIT License.
