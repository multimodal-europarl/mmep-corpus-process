#!/usr/bin/env python3
"""
Reinstall pymmep to the working virtual environment.

(This is depreciated after release of pymmep on PyPI,
but potentially still usefull during development)

NB, this will take pymmep from whatever branch of the pymmep
repo that's currently checked out locally.
"""
import argparse, os, shutil




def main(args):
    """
```
usage:
reinstall-pymmep.py [-h] [-e ENV_PATH] [-p PYTHON_VERSION]

Reinstall pymmep to the working virtual environment.

(This is depreciated after release of pymmep on PyPI,
but potentially still usefull during development)

NB, this will take pymmep from whatever branch of the pymmep
repo that's currently checked out locally.

options:
  -h, --help            show this help message and exit
  -e ENV_PATH, --env-path ENV_PATH
                        Path to working Python environment.
  -p PYTHON_VERSION, --python-version PYTHON_VERSION
                        Python version in working environment
```
    """
    ignore = [
        ".git",
        ]
    src = "pymmep/pymmep/"
    dest = f"{args.env_path}lib/python{args.python_version}/site-packages/pymmep/"
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest,
                    ignore = shutil.ignore_patterns(*ignore),
                    dirs_exist_ok = True
        )




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-e", "--env-path",
                        type=str,
                        default="../mmepenv/",
                        help="Path to working Python environment."
        )
    parser.add_argument("-p", "--python-version",
                        type=str,
                        default="3.11",
                        help="Python version in working environment"
        )
    args = parser.parse_args()
    main(args)
