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

#### Prerequisites

#### Install thru Pip

```bash
git clone https://github.com/radoslavraynov/macaulay2-jupyter-kernel m2kj
cd m2jk
python3 -m m2_kernel.install
```

#### Install from Source

## License

This software is not part of Macaualay2 and is released under the MIT License.
