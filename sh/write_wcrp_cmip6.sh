#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "writing WCRP cmip6 vocabs ..."

	python $PYESSV_LIB_HOME/sh/write_wcrp_cmip6_vocabs.py --source=$WCRP_CMIP6_VOCABS
	log "WCRP cmip6 vocabs written to "$HOME/.esdoc/pyessv-archive

	python $PYESSV_LIB_HOME/sh/write_wcrp_cmip6_bash_vars.py
	log "WCRP cmip6 vocabs bash file written to "$PYESSV_LIB_HOME/sh/write_wcrp_cmip6_bash_vars_output.sh
}

# Invoke entry point.
main
