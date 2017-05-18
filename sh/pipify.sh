#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	cd $PYESSV_LIB_HOME
	python ./setup.py sdist upload
	log "library uploaded to pypi"
}

# Invoke entry point.
main
