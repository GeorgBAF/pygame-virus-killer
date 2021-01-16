from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "main2.py"}],
)

# setup(
#    options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
#    windows = [{'script': "main2.py"}],
#    zipfile = None,
#)

#setup(
#    options = {'py2exe': {'bundle_files': 3}},
#    windows = [{'script': "main2.py"}],
#    zipfile = None,
#)