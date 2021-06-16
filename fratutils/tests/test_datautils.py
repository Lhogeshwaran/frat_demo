import pytest
from .. import datautils

def test_real_core():
    assert datautils.PreProcessing().check_is_core(3131) == 1
