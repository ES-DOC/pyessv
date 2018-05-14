#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	rm $PYESSV_LIB_HOME/ops/logs/*.log

	log "logs reset"
}

# Invoke entry point.
main
