from multiprocessing.sharedctypes import Value
import pyessv
from pyessv.parsing.identifiers.config import get_config
from pyessv.parsing.identifiers.config import ParsingConfiguration
from pyessv.parsing.identifiers.config import ParsingSpecification


def test_that_parsing_configuration_file_can_be_decoded():
    # TODO: instead of top down scan use io-manager to scan from file system directly.
    for authority in pyessv.load():
        for scope in authority:
            for identifier_type in pyessv.IDENTIFIER_TYPE_SET:
                try:
                    cfg = get_config(scope, identifier_type)
                except FileNotFoundError:
                    print(scope, identifier_type)
                    # Not all identifier types are implemented across all scopes.
                    continue
                else:
                    assert isinstance(cfg, ParsingConfiguration)
                    for spec in cfg.specs:
                        assert isinstance(spec, ParsingSpecification), spec
