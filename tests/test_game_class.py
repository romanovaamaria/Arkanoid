import pytest
import pygame
from main import game

def test_game_invalid_input():
    #Test if game raises TypeError when an invalid input is given
    with pytest.raises(TypeError):
        game('level 1')