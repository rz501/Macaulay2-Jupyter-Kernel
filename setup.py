from distutils.core import setup

setup(
    name='m3_kernel',
    version='0.1',
    packages=['m3_kernel'],
    description='Macaulay2 kernel for Jupyter (test)',
    long_description='add later',
    author='Radoslav Raynov',
    author_email='radoslav@math.cornell.edu',
    url='https://github.com/radoslavraynov/macaulay2-jupyter-kernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[],
)
