""" Macaulay2 Jupyter Kernel: version

Unlike most packages, __version__ can not simply be put in __init__.py
The latter imports the kernel class, which in turn instantiates a whole bunch.
To preserve single-source definition, we compromise with calling `exec`
for example, see https://packaging.python.org/guides/single-sourcing-package-version
"""

__version__ = '0.1.1'
