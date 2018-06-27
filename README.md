# M2JK

You can now use [Jupyter](http://www.jupyter.org) (Notebook or Lab) as a front-end for [Macaulay2](http://faculty.math.illinois.edu/Macaulay2/).
<!-- It can be used as a drop-in replacement for Emacs,
Unlike Emacs or M2's interactive session,
Jupyter provides mode
but introduces far more powerful features like
logical organization of your code into cells and inline Markdown with TeX,
to name just a couple. -->

For details, check out the [wiki](../../wiki).
For bugs or requests, open an issue.
For recent changes, see the [changelog](CHANGELOG.md).

![](/demo/screenshot.png?raw=true)

## Examples

Below are a few sample notebooks all highlighting different key points.
You can view them directly on Github,
however, the output is rendered as plain text.

* [minimal demo](demo/minimal.ipynb) (the notebook in the screenshot)
* [intro to the Macaulay2 book](demo/p1m2book.ipynb)
* [examples of a new coding style](demo/newstyle.ipynb)
* [a sample Python notebook](demo/demo-python.ipynb)

## Installation

### Prerequisites

Quite obviously, you need recent versions of both Macaulay2 and Jupyter installed on your system.
You can find installation instructions on their respective sites.

Further, `M2` must be on your `PATH`.
If you are using Emacs as your front-end, it already is.
Otherwise, you can achieve that by running `setup()` from within an M2 session.
(You might have to restart your machine in that case.)

### Install

You can install the kernel directly thru `pip` by

```
$ pip3 install m2jk
$ python3 -m m2_kernel.install
```

Alrernatively, you can install it from source by

```bash
$ git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel.git m2jk
$ cd m2jk
$ python3 setup.py install # --record files.txt
$ python3 -m m2_kernel.install
```

### Run on Jupyter

Once installation is complete, you need to start (or restart) Jupyter by

```bash
$ jupyter notebook &
```

This shoud fire up a browser for you. If not, copy the output link into one.
Then select File ⇨ New Notebook ⇨ M2 from the main menu.

### [Migrate from Emacs to Jupyter](../../wiki/migrate-from-emacs)

<!-- Not so much as an IDE but more as an environment to quickly try out ideas in
You can find detailed instructions how to migrate your `.m2` files into the Jupyter coding style
[here](../../wiki/Migrate).
Note that you can always export a Jupyter notebook (back) to `.m2`. -->

## License

This software is not part of Macaulay2 and is released under the MIT License.
