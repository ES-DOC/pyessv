#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	source $PYESSV_LIB_HOME/sh/ws/daemon_stop.sh
	source $PYESSV_LIB_HOME/sh/ws/daemon_start.sh
}

# Invoke entry point.
main
