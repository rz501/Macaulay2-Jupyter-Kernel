from ipykernel.kernelapp import IPKernelApp
from . import M2Kernel

IPKernelApp.launch_instance(kernel_class=M2Kernel)
