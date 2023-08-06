#!/usr/bin/env python

import pytest

# some global settings

# tests
@pytest.mark.usefixtures("aiida_env")
class Test_kkr_parser():
    """
    Tests for the kkr parser
    """
    
    def test_parse_kkr_calc(self):
        """
        ...
        """
        from aiida.orm import load_node
        from aiida_kkr.parsers.kkr import KkrParser
        from aiida.orm.importexport import import_data
        import_data('files/db_dump_kkrcalc.tar.gz')
        kkr_calc = load_node('3058bd6c-de0b-400e-aff5-2331a5f5d566')
        parser = KkrParser(kkr_calc)
        success, outnodes = parser.parse_from_calc()
        assert success
