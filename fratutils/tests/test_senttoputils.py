import pytest
from .. import senttoputils

def test_frat_topics_others():
    '''Testing to ensure core item contains others as this is hardcoded in source-code.'''
    message = '"Others" category is hardcoded in source-code and should not be removed from frat_config.'
    assert 'others' in senttoputils.Topic().cfg['frat_topics'], message
