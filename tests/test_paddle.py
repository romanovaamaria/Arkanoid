import pygame
from main import paddle
from pygame.locals import *

def test_paddle_init():
    screen_width = 800
    screen_height = 600
    paddle_size = 0.2
    paddle_color = (255, 255, 255)
    test_paddle = paddle(screen_width, screen_height, paddle_size, paddle_color)
    assert test_paddle.width == int(screen_width * paddle_size / 3)
    assert test_paddle.height == 30
    assert test_paddle.x == int((screen_width / 2) - (test_paddle.width / 2))
    assert test_paddle.y == screen_height - (test_paddle.height * 2)
    assert isinstance(test_paddle.rect, pygame.Rect)
    assert test_paddle.paddle_color == paddle_color

def test_paddle_move():
    pad = paddle(screen_width=800, screen_height=600, paddle_size=1, paddle_color=(255, 255, 255))
    mouse_position = (400, 0)
    pad.move(mouse_position)
    assert pad.rect.x == 400 - pad.width/2
