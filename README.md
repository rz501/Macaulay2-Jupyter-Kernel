# M2JK

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).
Aside from a drop-in replacement for Emacs or M2's interactive session,
Jupyter provides a number of features like code-organization,
inline Markdown with TeX and several different key-bindings,
to name just a few.

For details, check out the [wiki](../../wiki).
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

![](/demo/screenshot.png?raw=true)

## Disclaimer

The project is still in the alpha phase, so crashes and data loss may occur!

## Examples

Below are a few sample notebooks all highlighting different key points.

* [minimal demo](http://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/minimal.ipynb) (the notebook in the screenshot)
* [preface to the Macaulay2 book](http://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/p1m2book.ipynb)
* [examples of a new coding style](http://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/newstyle.ipynb)
* [a sample Python notebook](http://nbviewer.jupyter.org/github/radoslavraynov/Macaulay2-Jupyter-Kernel/blob/master/demo/demo-python.ipynb)

Note that while the files above are statically rendered locally
and reside on Github,
they are displayed thru [nbviewer.jupyter.org](#)
since Github seems to only support plain text output.
In particular, client-side syntax highlighting, such as in the screenshot,
is missing completely.

## Installation

### Prerequisites

The project runs on Python3.

Also, quite obviously, you need recent versions of both Macaulay2 and Jupyter installed on your system.
You can find installation instructions on their respective sites.

Further, `M2` must be on your `PATH`.
If you are using Emacs as your front-end, it already is.
Otherwise, you can achieve that by running `setup()` from within an M2 session.
See [here](../../wiki/installation-details) for details.

### Install

You can install the stable version of the kernel directly by

```
$ pip3 install m2jk
$ python3 -m m2_kernel.install
```

Alrernatively, you can install the latest version from source by

```bash
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel.git m2jk
$ pip3 install m2jk
$ python3 -m m2_kernel.install
```

### Run on Jupyter

Once installation is complete, you need to start (or restart) Jupyter by

```bash
$ jupyter notebook &
```

This shoud fire up a browser for you. If not, copy the output link into one.
Then select File ⇨ New Notebook ⇨ M2 from the main menu.

## FAQ

* [Migrate from Emacs to Jupyter](../../wiki/migrate-from-emacs)
* [Known Issues](../../wiki/caveats)
* [Todo List](TODO)

## License

This software is not part of Macaulay2 and is released under the MIT License.
