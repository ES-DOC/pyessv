#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	python $PYESSV_LIB_HOME/sh/wcrp/cmip6/write_model_seeding_config.py
	log "WCRP cmip6 model seeding config files written to "$ESDOC_HOME/repos/institutional
}

# Invoke entry point.
main