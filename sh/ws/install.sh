#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	_install_ops_dir
	_install_config
	log "web-service installed"
}

_install_ops_dir()
{
	mkdir -p $PYESSV_LIB_HOME/ops
	mkdir -p $PYESSV_LIB_HOME/ops/ws/config
	mkdir -p $PYESSV_LIB_HOME/ops/ws/daemon
	mkdir -p $PYESSV_LIB_HOME/ops/ws/logs
	log "ops directory initialized"
}

_install_config()
{
	cp $PYESSV_LIB_HOME/resources/ws.conf $PYESSV_LIB_HOME/ops/ws/config
	log "configuration files initialized"
}

# Invoke entry point.
main
