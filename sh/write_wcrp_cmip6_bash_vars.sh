#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $PYESSV_LIB_HOME/sh/write_wcrp_cmip6_bash_vars.py
}

# Invoke entry point.
main $1
