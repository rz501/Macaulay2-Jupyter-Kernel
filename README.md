# M2JK

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).
It can be used as a drop-in replacement for Emacs,
but introduces far more powerful features like
logical organization of the code into cells and in-line Markdown with TeX,
to name just a couple.

For details, check out the [documentation](http://m2jk.rtfd.io).
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

![](/demo/screenshot.png)

## Examples

Below are a few sample notebooks all highlighting different key points.
You can view them directly on Github but the output is rendered as plain text.

* [minimal demo](demo/minimal.ipynb) (the notebook in the screenshot)
* [intro to the Macaulay2 book](demo/m2book.ipynb)
* [examples of a new coding style](demo/newstyle.ipynb)
* [a sample Python notebook](demo/demo-python.ipynb)

## Installation

##### Prerequisites

Quite obviously, you need to have recent versions of both Macaulay2 and Jupyter installed on your system.
You can find installation instructions for your environment on their respective sites.

Further, `M2` must be on your `PATH`. It already is if you are using it with Emacs. Otherwise, you can achieve that by running `setup()` from within an M2 session; and you might have to restart your machine adter that.

### Install thru Pip

```
$ pip3 install m2kj
```

### Install from Source

```
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel m2kj
$ cd m2jk
$ python3 -m m2_kernel.install
```

###### Run on Jupyter

Once installation is complete, you need to start (or restart) Jupyter by

```
$ jupyter notebook
```

and then select from the main menu File ⇨ New Notebook ⇨ M2.

## License

This software is not part of Macaualay2 and is released under the MIT License.
