from ipykernel.kernelapp import IPKernelApp
from . import M2Kernel

""" Macaulay2 Jupyter Kernel point of entry
"""

IPKernelApp.launch_instance(kernel_class=M2Kernel)
