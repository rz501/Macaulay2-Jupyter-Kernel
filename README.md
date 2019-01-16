# M2JK

[![Build Status](https://img.shields.io/travis/radoslavraynov/Macaulay2-Jupyter-Kernel.svg?style=flat-square)](https://travis-ci.org/radoslavraynov/Macaulay2-Jupyter-Kernel)

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).
Aside from a drop-in replacement for Emacs or M2's interactive session,
Jupyter provides a number of features like
code organization, inline Markdown with TeX and different *standard* key-bindings,
to name just a few.
<!-- With minimal additional setup, -->
<!-- it can even support multiple users on a shared session over a local network or the Internet. -->

For details, check out the [wiki](../../wiki).
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

![](/demo/screenshot.png?raw=true)

## Examples

Below are a few sample notebooks all highlighting different key points.

* [minimal demo](https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/minimal.ipynb) (the notebook in the screenshot)
* [preface to the Macaulay2 book](https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/p1m2book.ipynb)
* [examples of the new features](https://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/newstyle.ipynb)

Note that while the files above are statically rendered locally
and reside on Github,
they are displayed thru [nbviewer](#)
since Github seems to only support plain text output.
In particular, client-side syntax highlighting, such as in the screenshot,
is missing completely.

## Installation

### Prerequisites

The project runs on Python version 3.6+.
Also, quite obviously, you need recent versions of both Macaulay2 and Jupyter installed on your system.
You can find installation instructions on their respective sites.

Further, `M2` must be on your `PATH`.
If you are using Emacs as your front-end, it already is.
Otherwise, you can achieve that by running `setup()` from within an M2 session.

### Install

You can install the latest version from source by

```bash
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel.git
$ pip3 install macaulay2-jupyter-kernel/ # keep the forward slash or cd into to the directory 
$ python3 -m m2_kernel.install
```

### Run on Jupyter

Once installation is complete, you need to start (or restart) Jupyter by

```bash
$ jupyter notebook &
```

This shoud fire up a browser for you. If not, copy the output URL into one.
Then select File ⇨ New Notebook ⇨ M2 from the main menu.

## License

This software is not part of Macaulay2 and is released under the MIT License.
