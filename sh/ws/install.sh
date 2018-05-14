#!/bin/bash

# Import utils.
source $PYESSV_LIB_HOME/sh/utils.sh

# Main entry point.
main()
{
	_install_ops_dir
	_install_config
	_install_venv
	log "web-service installed"
}

_install_ops_dir()
{
	mkdir -p $PYESSV_LIB_HOME/ops
	mkdir -p $PYESSV_LIB_HOME/ops/config
	mkdir -p $PYESSV_LIB_HOME/ops/daemon
	mkdir -p $PYESSV_LIB_HOME/ops/logs
	log "ops directory installed"
}

_install_config()
{
	cp $PYESSV_LIB_HOME/resources/*.conf $PYESSV_LIB_HOME/ops/config
	log "configuration files installed"
}

_install_venv()
{
    log "installing virtual environment ..."

    # ... install venv.
    $PYESSV_WS_PIP install --upgrade pip
    $PYESSV_WS_PIP install --upgrade virtualenv
    virtualenv $PYESSV_LIB_HOME/ops/venv

    # ... install dependencies.
    source $PYESSV_LIB_HOME/sh/ws/activate_venv.sh
    $PYESSV_WS_PIP install --upgrade pip
    $PYESSV_WS_PIP install --upgrade --no-cache-dir -I -r $PYESSV_LIB_HOME/requirements.txt

    deactivate
	log "virtual environment installed"
}

# Invoke entry point.
main
