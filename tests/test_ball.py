import pytest
from pygame.locals import Rect
from main import brick_wall, ball, screen_width, screen_height


def test_ball_default():
    # create an instance of the class
    obj = ball(20, 40)
    # set some non-default values
    obj.ball_radius = 15
    obj.speed_x = 5
    obj.speed_y = -5
    obj.game = 1

    obj.default(10, 20)
    assert obj.ball_radius == 14
    assert obj.x == 10 - obj.ball_radius
    assert obj.y == 20
    assert obj.rect == Rect(obj.x, obj.y, obj.ball_radius * 2, obj.ball_radius * 2)
    assert obj.speed_x == 1
    assert obj.speed_y == -1
    assert obj.game == 0


# create a test brick wall
test_wall = brick_wall(level=1)
test_wall.create_wall(6,6)

# create a test ball object
test_ball = ball(x=screen_width // 2, y=screen_height // 2)

# define the test cases
test_cases = [
    # test that ball collides with brick and its strength reduces by 1
    {"ball_x": test_wall.rows_of_bricks[1][2].left + test_wall.rows_of_bricks[1][2].width // 2,
     "ball_y": test_wall.rows_of_bricks[1][2].top + test_wall.rows_of_bricks[1][2].height + test_ball.ball_radius,
     "expected_strength": test_wall.rows_of_bricks[1][2].strength - 1},

    # test that ball destroys brick when strength is reduced to 0
    {"ball_x": test_wall.rows_of_bricks[2][2].left + test_wall.rows_of_bricks[2][2].width // 2,
     "ball_y": test_wall.rows_of_bricks[2][2].top + test_wall.rows_of_bricks[2][2].height + test_ball.ball_radius,
     "expected_strength": 0},
]


# define the test function
@pytest.mark.parametrize("test_case", test_cases)
def test_ball_collision_and_destruction_strength(test_case):
    # reset ball position
    test_ball.default(test_case["ball_x"], test_case["ball_y"])

    # set the strength of the test brick based on the expected strength
    test_wall.rows_of_bricks[1][2].strength = test_case["expected_strength"]

    # call the ball move function
    test_ball.move(wall=test_wall)

    # check the brick's strength value for brick collisions
    if "expected_strength" in test_case:
        assert test_wall.rows_of_bricks[1][2].strength == test_case["expected_strength"]


# define the test cases
test_cases = [
    # test that ball bounces off top wall
    {"ball_x": screen_width // 2,
     "ball_y": test_ball.ball_radius + 1,
     "expected_speed_y": 1},

    # test that ball bounces off left wall
    {"ball_x": test_ball.ball_radius + 1,
     "ball_y": screen_height // 2,
     "expected_speed_x": 1},

    # test that ball bounces off right wall
    {"ball_x": screen_width - test_ball.ball_radius - 1,
     "ball_y": screen_height // 2,
     "expected_speed_x": -1},
]


# define the test function
@pytest.mark.parametrize("test_case", test_cases)
def test_ball_collision_and_destruction_speed(test_case):
    test_ball.default(test_case["ball_x"], test_case["ball_y"])

    # check the ball's speed values for wall collisions
    if "expected_speed_x" in test_cases:
        assert test_ball.speed_x == test_case["expected_speed_x"]
    if "expected_speed_y" in test_cases:
        assert test_ball.speed_y == test_case["expected_speed_y"]

    # store the original speeds of the ball
    original_speed_x = test_ball.speed_x
    original_speed_y = test_ball.speed_y

    # reset the original speeds of the ball
    test_ball.speed_x = original_speed_x
    test_ball.speed_y = original_speed_y
