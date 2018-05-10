#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "running ..."

    python $PYESSV_LIB_HOME/sh/ws/run.py
}

# Invoke entry point.
main
