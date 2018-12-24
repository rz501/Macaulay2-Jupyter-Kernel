from distutils.core import setup
from distutils.command.install import install

__version__ = "0.1.0"
exec(open("./m2_kernel/version.py").read())  # see comment in file

# class install_with_kernelspec(install):
#     def run(self):
#         install.run(self)
#         from m2_kernel import install as kernel_install
#         kernel_install.install_my_kernel_spec()


setup(
    name='macaulay2_jupyter_kernel',
    version=__version__,
    packages=['m2_kernel'],
    description='Macaulay2 kernel for Jupyter',
    long_description='add later',
    author='Radoslav Raynov',
    author_email='radoslav.raynov@yahoo.com',
    url='https://github.com/radoslavraynov/macaulay2-jupyter-kernel',
    # packages=find_packages(),
    install_requires=['ipykernel', 'notebook', 'pexpect'],
    # cmdclass={'install': install_with_kernelspec},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.7',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License'
    ]
)
