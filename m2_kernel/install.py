import argparse
import json
import os
import sys

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory
from notebook import __path__ as notebook_pkgdir
from notebook.nbextensions import install_nbextension, enable_nbextension

""" Macaulay2 Jupyter Kernel: standard jupyter kernel spec installation
"""

kernel_json = {
    "argv": [sys.executable, "-m", "m2_kernel", "-f", "{connection_file}"],
    "display_name": "M2",
    "language": "text/x-macaulay2",
    "codemirror_mode": "macaulay2",
}


def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)

        print('Installing kernel spec ...')
        KernelSpecManager().install_kernel_spec(td, 'm2', user=user, prefix=prefix)

        srcdir = '{}/data/'.format(os.path.dirname(__file__))
        dstdir = '{}/static/components/codemirror/mode/'.format(notebook_pkgdir[0])

        # to avoid getting a GET 404 error, m2-mode must be on both paths...
        print("Installing nbextension for syntax highlighting ...")
        install_nbextension(srcdir+'m2-mode', overwrite=True, symlink=True,
                            nbextensions_dir=dstdir, destination='macaulay2')
        # may if you never enable it, there'd be no GET 404
        install_nbextension(srcdir+'m2-mode', overwrite=True, symlink=True, user=user)
        enable_nbextension('notebook', dstdir+'m2-mode/main')


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--user', action='store_true',
                    help="Install to the per-user kernels registry. Default if not root.")
    ap.add_argument('--sys-prefix', action='store_true',
                    help="Install to sys.prefix (e.g. a virtualenv or conda env)")
    ap.add_argument('--prefix',
                    help="Install to the given prefix."
                         "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/")
    args = ap.parse_args(argv)

    if args.sys_prefix:
        args.prefix = sys.prefix
    if not args.prefix and not _is_root():
        args.user = True

    install_my_kernel_spec(user=args.user, prefix=args.prefix)


if __name__ == '__main__':
    main()
