#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	pushd $PYESSV_LIB_HOME
	pipenv run python ./setup.py sdist upload
	log "library uploaded to pypi"
}

# Invoke entry point.
main
