#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $PYESSV_LIB_HOME/sh/writers/esgf-publisher/map.py --source=$1
	log "ESGF config vocabs written to "$HOME/.esdoc/pyessv-archive
}

# Invoke entry point.
main $1
