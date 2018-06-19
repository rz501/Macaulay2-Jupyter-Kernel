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

### Prerequisites

Quite obviously, you need to have recent versions of both Macaulay2 and Jupyter installed on your system.
You can find installation instructions for your environment on their respective sites.

Further, `M2` must be on your `PATH`. It already is, if you are using Emacs as your front-end.
Otherwise, you can achieve that by running `setup()` from within an M2 session.
(You might have to restart your machine in the latter case.)

Finally, you need Python3.6+. Note that Jupyter itself can do away with either version 2 or 3.

### Install

You can install the kernel directly thru `pip` by

```
$ pip3 install m2kj
```

Alrernatively, you can install it from source by

```
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel.git m2kj
$ cd m2jk
$ python3 -m m2_kernel.install
```

### Run on Jupyter

Once installation is complete, you need to start (or restart) Jupyter by

```
$ jupyter notebook
```

This may or may not open a browser for you. If not, copy the output link into one.
Then select File ⇨ New Notebook ⇨ M2 from the main menu.
Enjoy!

## License

This software is not part of Macaualay2 and is released under the MIT License.
