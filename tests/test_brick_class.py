import pytest
import pygame
from main import brick

def test_brick_init():
    b = brick(2, 3, 1, 5, 200)
    assert b.col == 2
    assert b.row == 3
    assert b.strength == 1
    assert b.width == 40
    assert b.height == 45
    assert b.rect == pygame.Rect(2 * 40, 3 * 45, 40, 45)
    assert b.left == 2 * 40
    assert b.right == 2 * 40 + 40
    assert b.top == 3 * 45
    assert b.bottom == 3 * 45 + 45

@pytest.mark.parametrize("col, row, strength, columns, screen_width", [
    (2, -3, 1, 5, 200),
    (2, 3, -1, 5, 200),
    (2, 3, 0, 5, 200)
])
def test_brick_init_invalid_input_value_error(col, row, strength, columns, screen_width):
    with pytest.raises(ValueError):
        brick(col, row, strength, columns, screen_width)
  
def test_brick_init_invalid_input_type_error():
    with pytest.raises(TypeError):
        brick("2", 3, 1, 5, 200)