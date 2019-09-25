#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYESSV_LIB_HOME:$PYTHONPATH
	source $PYESSV_LIB_VENV/bin/activate
}

# Invoke entry point.
main
