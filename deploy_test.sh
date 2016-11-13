#!/bin/bash
HOME="/home/thorsten/Dropbox/Entwickeln/Python_3/ablaufplus"
cd $HOME
echo "change to directory:" $PWD
echo "--------------------------------------------------"
# create binary distribution
python setup.py bdist

# create source distribution
python setup.py sdist

# register at pypitest
# python setup.py register -r pypitest

# deploy to pypitest
# python setup.py sdist upload -r pypitest
