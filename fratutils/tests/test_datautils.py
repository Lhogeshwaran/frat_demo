import pytest
from .. import datautils

def test_core_items():
    '''Second layer testing to ensure core item changes are intentional.'''
    actual = datautils.PreProcessing().cfg['core_items']
    expected = [3707, 3708, 3131, 3709, 1053, 1070]
    message = f'Expected {expected}, but got {actual}. If frat_config change is intentional, append change to test module.'
    assert actual == expected, message

def test_frat_topics():
    '''Testing to ensure core item changes are intentional.'''
    assert datautils.PreProcessing().cfg['frat_topics'] == ["subject", "lecture", "assignment", "time", "content", "others"]
