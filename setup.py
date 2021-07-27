# -*- coding: UTF-8 -*-
#! /usr/bin/python

from pathlib import Path
from setuptools import setup, find_packages
import atexit
from setuptools.command.install import install

def _post_install():
    from pyccel.compilers.generate_default import generate_default
    generate_default()


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)

# ...
# Read library version into '__version__' variable
path = Path(__file__).parent / 'pyccel' / 'version.py'
exec(path.read_text())
# ...

NAME    = 'pyccel'
VERSION = __version__
AUTHOR  = 'Pyccel development team'
EMAIL   = 'pyccel@googlegroups.com'
URL     = 'https://github.com/pyccel/pyccel'
DESCR   = 'Python extension language using accelerators.'
KEYWORDS = ['math']
LICENSE = "LICENSE"

setup_args = dict(
    name                 = NAME,
    version              = VERSION,
    description          = DESCR,
    long_description     = open('README.rst').read(),
    author               = AUTHOR,
    author_email         = EMAIL,
    license              = LICENSE,
    keywords             = KEYWORDS,
    url                  = URL,
)

# ...
packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])
# ...

# Dependencies
install_requires = [
    'numpy',
    'sympy>=1.2',
    'termcolor',
    'textx>=1.6',
    'filelock'
]

def setup_package():

    setup(packages=packages, \
          include_package_data=True, \
          install_requires=install_requires, \
          entry_points={'console_scripts': ['pyccel = pyccel.commands.console:pyccel', 'pyccel-clean = pyccel.commands.pyccel_clean:pyccel_clean_command']}, \
          cmdclass={'install': new_install},
          **setup_args)


if __name__ == "__main__":
    setup_package()
