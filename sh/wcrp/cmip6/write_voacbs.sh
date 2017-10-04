#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $PYESSV_LIB_HOME/sh/wcrp/cmip6/write_vocabs.py --source=$WCRP_CMIP6_VOCABS
	log "WCRP cmip6 vocabs written to "$HOME/.esdoc/pyessv-archive
}

# Invoke entry point.
main
