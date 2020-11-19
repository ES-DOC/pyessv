#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	pushd $PYESSV_LIB_HOME
	# pipenv run python ./setup.py sdist upload
	pipenv run python ./setup.py sdist bdist_wheel
	python3 -m twine upload --repository pypi dist/*

	log "library uploaded to pypi"
}

# Invoke entry point.
main
