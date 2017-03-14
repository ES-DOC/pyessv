#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	cd $PYESSV_LIB_HOME/notebooks
	jupyter notebook

    log "jupyter notebook server launched"
}

# Invoke entry point.
main