#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	# Reset vocabs.
	rm -rf ~/.esdoc/pyessv-archive/esdoc

	# Write vocabularies.
	source $PYESSV_LIB_HOME/sh/activate_venv.sh
	python $PYESSV_LIB_HOME/sh/writers/esdoc/write_errata.py
	python $PYESSV_LIB_HOME/sh/writers/esdoc/write_cmip6.py

	log "ES-DOC vocabs written to "$HOME/.esdoc/esdoc
}

# Invoke entry point.
main $1
