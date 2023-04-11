import pytest
from main import game

def test_game_invalid_input():
    with pytest.raises(ValueError):
        game(3)  # ensure invalid input raises ValueError
