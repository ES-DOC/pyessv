#!/bin/sh

PYESSV_LIB_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $PYESSV_LIB_HOME
export PYTHONPATH=PYTHONPATH:$PYESSV_LIB_HOME

nosetests -v -s tests
# nosetests -v -s tests/test_cache.py
# nosetests -v -s tests/test_codecs.py
# nosetests -v -s tests/test_factory.py
# nosetests -v -s tests/test_interface.py
# nosetests -v -s tests/test_io_manager.py
# nosetests -v -s tests/test_model.py
# nosetests -v -s tests/test_parse_identifiers.py
# nosetests -v -s tests/test_parser_name.py
# nosetests -v -s tests/test_parser_template.py
# nosetests -v -s tests/test_validation.py
