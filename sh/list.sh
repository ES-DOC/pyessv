#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "list archive starts ..."

	python $PYESSV_LIB_HOME/sh/list.py --authority=$1 --scope=$2 --collection=$3 --term=$4
}

# Invoke entry point.
main $1 $2 $3 $4
