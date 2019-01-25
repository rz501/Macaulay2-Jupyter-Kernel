from setuptools import setup
from m2_kernel import __version__


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='macaulay2-jupyter-kernel',
    version=__version__,
    packages=['m2_kernel'],
    description='Jupyter kernel for Macaulay2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Radoslav Zlatev',
    author_email='radoslav.raynov@yahoo.com',
    url='https://github.com/radoslavraynov/macaulay2-jupyter-kernel',
    # packages=find_packages(),
    install_requires=['ipykernel', 'notebook', 'pexpect'],
    include_package_data=True,
    package_data={'m2_kernel': ['data/m2-mode/*.js', 'data/m2-code/*.m2']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License'
    ]
)
