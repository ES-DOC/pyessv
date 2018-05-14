#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	source $PYESSV_LIB_HOME/sh/ws/reset_logs.sh
	supervisord -c $PYESSV_LIB_HOME/ops/config/supervisord.conf
	log "initialized web-service daemon"

	sleep 3.0
	source $PYESSV_LIB_HOME/sh/ws/daemon_status.sh
}

# Invoke entry point.
main
