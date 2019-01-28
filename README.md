# M2JK — Jupyter kernel for Macaulay2

[![](https://img.shields.io/travis/radoslavraynov/Macaulay2-Jupyter-Kernel.svg?style=flat-square)](https://travis-ci.org/radoslavraynov/Macaulay2-Jupyter-Kernel/)
[![](https://img.shields.io/pypi/v/macaulay2-jupyter-kernel.svg?style=flat-square)](https://pypi.org/project/macaulay2-jupyter-kernel/)
[![](https://img.shields.io/github/commits-since/radoslavraynov/macaulay2-jupyter-kernel/latest.svg?style=flat-square)](#)

> Beta Testing!

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).

See the [demo][demo] for sample use and an outline of the kernel-specific features.
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

[![](/demo/screenshot1.png)](/demo/screenshot1.png?raw=true)

## Requirements

You need a recent version of Python and `pip`.
Python 3 is recommended for build installs and necessary for source installs.
You can install Jupyter directly from PyPI by
```bash
pip3 install --upgrade pip
pip3 install jupyter
```

Macaulay2 needs to be installed and on your path.
If you are using Emacs as your front-end, it already is, but you can test it by `which M2`.
Otherwise, you can achieve that by running `setup()` from within an M2 session.
Alternatively, you can configure M2JK to use a specific binary.

## Installation

You can install the latest release version directly from PyPI by

```bash
$ pip3 install macaulay2-jupyter-kernel
$ python3 -m m2_kernel.install
```

Alternatively, you can install the latest development version from source by

```bash
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel.git
$ cd macaulay2-jupyter-kernel
$ pip3 install .
$ python3 -m m2_kernel.install
```

## Running the notebook

Once the installation is complete, you need to start (or restart) Jupyter by

```bash
$ jupyter notebook &
```

This shoud fire up a browser for you. If not, copy the output URL into one.
Then select File ⇨ New Notebook ⇨ M2 from the main menu.

<!-- Note that while the notebooks from the [Examples](#Examples) section are
statically rendered locally and reside on Github,
they are displayed thru [nbviewer](https://nbviewer.jupyter.org)
since Github seems to only support plain text output.
This isn't a problem when using the default display mode.
On the other hand, client-side syntax highlighting, such as in the screenshots,
is missing entirely. -->

## License

This software is not part of Macaulay2 and is released under the MIT License.

[demo]: https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/demo.ipynb
[features]: https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/features.ipynb
[m2book]: https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/m2book.ipynb
