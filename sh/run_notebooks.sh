#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	pushd $PYESSV_LIB_HOME
	pipenv run jupyter notebook --notebook-dir ./notebooks

    log "jupyter notebook server launched"
}

# Invoke entry point.
main