#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $PYESSV_LIB_HOME/sh/wcrp/cmip6/write_bash_vars.py
	log "WCRP cmip6 vocabs bash file written to "$PYESSV_LIB_HOME/sh/wcrp/cmip6/write_bash_vars_output.sh
}

# Invoke entry point.
main