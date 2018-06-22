from distutils.core import setup
from m2_kernel import __version__

# add code to automatically install the jupyter kernel spec

setup(
    name='macaulay2_jupyter_kernel',
    version=__version__,
    packages=['m2_kernel'],
    description='Macaulay2 kernel for Jupyter (first version)',
    long_description='add later',
    author='Radoslav Raynov',
    author_email='radoslav.raynov@yahoo.com',
    url='https://github.com/radoslavraynov/macaulay2-jupyter-kernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License'
    ]
)
