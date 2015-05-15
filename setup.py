"""projector: sdffd

sfdds
"""
from __future__ import print_function
import os
from os.path import relpath, join
from distutils.version import StrictVersion
from setuptools import setup
DOCLINES = __doc__.split("\n")


#-----------------------------------------------------------------------------
VERSION = '0.1'
ISRELEASED = False
__version__ = VERSION
#-----------------------------------------------------------------------------


def find_package_data():
    staticfiles = []
    for root, dirnames, filenames in os.walk('projector/static'):
        for fn in filenames:
            staticfiles.append(relpath(join(root, fn), 'projector'))
    return staticfiles


def warn_on_version(module_name, minimum=None, package_name=None,
                    recommend_conda=True,  instructions=None):
    if package_name is None:
        package_name = module_name

    class VersionError(Exception):
        pass

    msg = None
    base = 'This package requires the python package "%s", '
    try:
        package = __import__(module_name)
        if minimum is not None:
            try:
                v = package.version.short_version
            except AttributeError:
                v = package.__version__
            if StrictVersion(v) < StrictVersion(minimum):
                raise VersionError
    except ImportError:
        if minimum is None:
            msg = (base + 'which is not installed.') % package_name
        else:
            msg = (base + 'version %s or later.') % (package_name, minimum)
    except VersionError:
        msg = (
            base + 'version %s or later. You have version %s installed. You will need to upgrade.') % (package_name, minimum, v)

    if instructions is not None:
        install = instructions
    elif recommend_conda:
        install = ('\nTo install %s, we recommend the conda package manger:\n\n'
                   '    $ conda install %s') % (package_name, package_name)
        install += '\n\nAlternatively, with pip you can install the package with:\n\n    $ pip install %s' % package_name
    else:
        install = '\nWith pip you can install the package with:\n\n    $ pip install %s' % package_name

    if msg:
        banner = ('==' * 40)
        print(
            '\n'.join([banner, banner, "", msg, install, "", banner, banner]))


setup(
    name='projector',
    author='Robert McGibbon',
    author_email='rmcgibbo@gmail.com',
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    version=__version__,
    packages=['projector'],
    package_data={'projector': find_package_data()},
    zip_safe=False,
    entry_points={'console_scripts': ['projector = projector.main:main']})

#warn_on_version('mdtraj', '0.8.0', recommend_conda=False)
#warn_on_version('sklearn', '0.9.0', package_name='scikit-learn')
#warn_on_version('flask', '0.9.0')
#warn_on_version('scipy', '0.9.0')
#warn_on_version('pylru', recommend_conda=False)
#warn_on_version('mixtape', instructions='Get mixtape from https://github.com/rmcgibbo/mixtape')
