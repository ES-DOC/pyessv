#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "listing @ "$1" ..."

	python $PYESSV_LIB_HOME/sh/list_terms.py --source=$1 --authority=$2 --scope=$3 --collection=$4
}

# Invoke entry point.
main $1 $2 $3 $4
