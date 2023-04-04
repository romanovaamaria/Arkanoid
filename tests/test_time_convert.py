import pytest
from main import time_convert


@pytest.mark.parametrize("seconds, expected_output", [(10, "0:0:10"),
                                                      (0, "0:0:0")])
def test_time_convert(seconds, expected_output):
    assert time_convert(seconds) == expected_output