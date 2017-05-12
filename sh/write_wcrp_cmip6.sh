#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "writing WCRP cmip6 vocabs ..."

	declare source=$1

	python $PYESSV_LIB_HOME/sh/write_wcrp_cmip6.py --source=$source

	log "WCRP cmip6 vocabs written to "$HOME/.esdoc/pyessv-archive
}

# Invoke entry point.
main $1
