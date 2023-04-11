import pytest
from main import gameover_menu


def test_gameover_menu_value_error():
    with pytest.raises(ValueError):
        gameover_menu(0, "invalid_time_string")
