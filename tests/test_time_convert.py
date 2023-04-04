import pytest
from main import time_convert

# test with different number of seconds
@pytest.mark.parametrize('seconds, expected_output', [(10, '0:0:10'),
                                                      (0, '0:0:0')])
def test_time_convert(seconds, expected_output):
    assert time_convert(seconds) == expected_output


# test with negative seconds to raise ValueError
def test_time_convert_error():
    with pytest.raises(ValueError):
        time_convert(-50)
