import pytest
import pygame
from main import brick, brick_wall

pygame.init()

def test_brick_wall_create_wall():
    bw = brick_wall(1)
    bw.create_wall(2, 3)
    assert len(bw.rows_of_bricks) == 3
    assert len(bw.rows_of_bricks[0]) == 2
    assert len(bw.rows_of_bricks[1]) == 2
    assert len(bw.rows_of_bricks[2]) == 2

def test_check_strength_easy():
    bw = brick_wall(1)
    bw.create_wall(3, 3)
    for row in bw.rows_of_bricks:
        for brick in row:
            assert brick.strength in [1]

def test_check_strength_hard():
    bw = brick_wall(2)
    bw.create_wall(3, 3)
    for row in bw.rows_of_bricks:
        for brick in row:
            assert brick.strength in [1, 2, 3]

def test_create_wall_range():
    # Test if the bricks are within the screen range
    bw = brick_wall(1)
    bw.create_wall(5, 5)
    screen_width = 640
    for row in bw.rows_of_bricks:
        for brick in row:
            assert 0 <= brick.rect.left <= screen_width
            assert 0 <= brick.rect.right <= screen_width