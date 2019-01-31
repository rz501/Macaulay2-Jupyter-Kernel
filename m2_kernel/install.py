import argparse
import json
import os
import shutil
import sys

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory
from notebook import __path__ as notebook_dir
from notebook.nbextensions import install_nbextension

""" Macaulay2 Jupyter Kernel: standard jupyter kernel spec installation
"""

kernel_json = {
    "argv": [sys.executable, "-m", "m2_kernel", "-f", "{connection_file}"],
    "display_name": "M2",
    "language": "text/x-macaulay2",
    "codemirror_mode": "macaulay2",
}


def install_kernel_assets(user=True, prefix=None):
    """
    """
    assets_dir = '{}/assets'.format(os.path.dirname(__file__))

    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, indent=2, sort_keys=False)
        shutil.copy('{}/m2-spec/kernel.js'.format(assets_dir), td)
        print('Installing kernel spec ...')
        KernelSpecManager().install_kernel_spec(td, kernel_name='m2', user=user, prefix=prefix)

    print("Installing nbextension for syntax highlighting ...")
    install_nbextension('{}/m2-mode'.format(assets_dir),
            nbextensions_dir='{}/static/components/codemirror/mode/'.format(notebook_dir[0]),
            destination='macaulay2', overwrite=True, symlink=False)


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

    install_kernel_assets(user=args.user, prefix=args.prefix)


if __name__ == '__main__':
    main()
