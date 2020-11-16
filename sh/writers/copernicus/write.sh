#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	pushd $PYESSV_LIB_HOME
	pipenv run python $PYESSV_LIB_HOME/sh/writers/copernicus/cordexp/write.py --source=$1
	log "COPERNICUS cordexp vocabs written to "$HOME/.esdoc/pyessv-archive
}

# Invoke entry point.
main $1
