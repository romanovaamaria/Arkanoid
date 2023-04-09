import pytest
import pygame
from main import draw_text

pygame.init()

@pytest.fixture
def screen():
    return pygame.display.set_mode((640, 480))

@pytest.mark.parametrize("text, font, color, x, y, expected_color", [
    ("Hello World", pygame.font.Font(None, 60), (255, 255, 255), 100, 100, (255, 255, 255, 255)),
    ("", pygame.font.Font(None, 60), (255, 255, 255), 200, 200, (0, 0, 0, 255)),
    ("This text is too large to fit on the screen", pygame.font.Font(None, 60), (255, 255, 255), 400, 400, (255, 255, 255, 255)),
    ("!@#%^&*()-_=+[];:',.<>/?|`~", pygame.font.Font(None, 60), (255, 255, 255), 100, 100, (255, 255, 255, 255)),
    ("0123456789", pygame.font.Font(None, 60), (255, 255, 255), 100, 100, (255, 255, 255, 255)),
])
def test_draw_text(screen, text, font, color, x, y, expected_color):
    draw_text(text, font, color, screen, x, y)
    assert screen.get_at((x+5, y+5)) == expected_color

    