#!/bin/sh

PYESSV_LIB_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $PYESSV_LIB_HOME
export PYTHONPATH=PYTHONPATH:$PYESSV_LIB_HOME
nosetests -v -s tests
