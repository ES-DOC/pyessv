#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "list terms starts ..."

	python $PYESSV_LIB_HOME/sh/list_terms.py --authority=$1 --scope=$2 --collection=$3

	log "list terms complete"
}

# Invoke entry point.
main $1 $2 $3
