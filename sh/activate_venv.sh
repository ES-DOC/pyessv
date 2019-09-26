#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYESSV_LIB_HOME:$PYTHONPATH
	venv_path=${PYESSV_LIB_VENV:-$PYESSV_LIB_HOME/ops/venv}
	source $venv_path/bin/activate
	log "venv activated @ "$venv_path
}

# Invoke entry point.
main
