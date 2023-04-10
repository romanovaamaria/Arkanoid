import sys

import pygame
import time
import random as rand
import argparse
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 700
paddle_size = 1
columns = 6
rows = 6

# default color palette
paddle_color = (224, 187, 228)
color1 = (254, 200, 216)
color2 = (210, 145, 188)
color3 = (149, 125, 173)

# setting screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arkanoid')

# setting background image
bg_img = pygame.image.load('backgr.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

# color change
parser = argparse.ArgumentParser()
parser.add_argument('--color', help='Change color palette', choices=['1', '2', '3', '4'])
args = parser.parse_args()

if args.color == '1':
    paddle_color = (224, 187, 228)
    color1 = (254, 200, 216)
    color2 = (210, 145, 188)
    color3 = (149, 125, 173)
elif args.color == '2':
    paddle_color = (247, 226, 203)
    color1 = (250, 214, 165)
    color2 = (247, 179, 156)
    color3 = (242, 150, 150)
elif args.color == '3':
    paddle_color = (111, 211, 252)
    color1 = (97, 168, 237)
    color2 = (62, 115, 206)
    color3 = (49, 66, 190)
elif args.color == '4':
    paddle_color = (143, 217, 168)
    color1 = (72, 191, 145)
    color2 = (21, 153, 122)
    color3 = (1, 121, 111)


def draw_text(str: str, font: int, color: tuple, screen, x: int, y: int):
    """   
    Displays text

    :param str: text
    :param font: size
    :param color: font color rgb 
    :param screen: surface 
    :param x: left-most x coordinate
    :param y: top y coordinate
    :returns: None
    """
    text = font.render(str, 1, color)
    textrect = text.get_rect()
    textrect.topleft = (x, y)
    screen.blit(text, textrect)


# func to transform seconds to minutes:seconds format
def time_convert(sec: int | float) -> str:
    """
    Converts seconds to hours-minutes-seconds format.

    :param sec: seconds given
    :returns: formatted string
    :rtype: str
    :raises ValueError: if sec is negative
    """
    if sec < 0:
        raise ValueError("sec must be a positive number")

    mins = sec // 60
    hours = mins // 60
    mins = mins % 60
    sec = sec - mins*60 - hours*3600
    return str("{0}:{1}:{2}".format(int(hours), int(mins), int(sec)))


class paddle():
    """
    Object paddle which will be moved by player
    """

    # default func is used for init
    def __init__(self):
        self.default()

    def draw(self):
        """
        Displaying paddle
        """
        pygame.draw.rect(screen, paddle_color, self.rect, 0, 5)

    def default(self):
        """
        Define paddle variables
        """
        self.height = 30
        self.width = int(screen_width * paddle_size / 3)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """
        Movement of paddle using mouse
        """
        pos = pygame.mouse.get_pos()
        x = pos[0] - self.width / 2
        if (x >= 0) and (x <= (screen_width - 100 - self.width / 2)):
            self.rect.x = x

    # object brick, from which wall is created


class brick():
    """
    Object brick, from which wall is created
    
    """

    def __init__(self, col: int, row: int, strength: int):
        """
        :param col: Number of columns
        :param row: Number of rows
        :param strength: The strength of brick(number of times it has to be hit to be destroyed completely)
        """
        self.col = col
        self.row = row
        self.strength = strength
        self.heigth = 45
        self.width = screen_width / columns
        self.rect = Rect(self.col * self.width, self.row * self.heigth, self.width, self.heigth)
        # replacement of rect methods that didn`t work`
        self.left = self.col * self.width
        self.right = self.col * self.width + self.width
        self.top = self.row * self.heigth
        self.bottom = self.row * self.heigth + self.heigth


class brick_wall():
    """
    Object - wall created from instances of BRICK class
    """

    # default func is used for init
    def __init__(self, level):
        self.level = level

    def draw_wall(self):
        """
        Defining the color of brick based on its strength and displaying it
        """
        for row in self.rows_of_bricks:
            for brick in row:
                if brick.strength == 1:
                    brick_col = color1
                elif brick.strength == 2:
                    brick_col = color2
                elif brick.strength == 3:
                    brick_col = color3
                pygame.draw.rect(screen, brick_col, brick.rect)
                pygame.draw.rect(screen, paddle_color, (brick.rect), 2)

    def create_wall(self):
        """
        Func used to create 2-d array of bricks
        """
        self.rows_of_bricks = []
        for row in range(rows):
            bricks = []
            # values of strength depend on level
            for col in range(columns):
                if self.level == 1:
                    strength = 1
                else:
                    strength = rand.randint(1, 3)
                current_brick = brick(col, row, strength)
                bricks.append(current_brick)
            self.rows_of_bricks.append(bricks)


class ball():
    # default func is used for init
    def __init__(self, x, y):
        self.default(x, y)

    def draw(self):
        """
        Draws a ball.

        :returns: None
        """
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius)

    # reset all the values
    def default(self, x: int | float, y: int | float) -> None:
        """
        Resets all the values to default positions.

        :param x: x coordinate
        :param y: y coordinate
        :returns: None
        :rtype: None
        """
        self.ball_radius = 14
        self.x = x - self.ball_radius
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 1
        self.speed_y = -1
        self.game = 0

    # the main logic of ball movements and colliding
    def move(self, wall: brick_wall) -> int:
        """
        Moves the ball to destroy the bricks.

        :param wall: The wall of bricks
        :return: win or lose condition
        :rtype: int
        """

        wall_destroyed = True
        # difference between blocks collided
        diff_between = 5

        # bounce from the sides and top
        if self.rect.right > screen_width or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        # fall at the bottom for game over condition
        if self.rect.bottom > screen_height:
            self.game = -1

        # collision with the paddle
        if self.rect.colliderect(current_paddle):
            if abs(self.rect.bottom - current_paddle.rect.top) < diff_between and self.speed_y > 0:
                self.speed_y *= -1
            else:
                self.speed_x *= -1

        for row in wall.rows_of_bricks:
            for item in row:
                # check if there was a collision and from which side
                if self.rect.colliderect(item.rect):
                    if abs(self.rect.bottom - item.top) < diff_between and self.speed_y > 0:
                        self.speed_y *= -1
                        # change brick strength
                        if item.strength > 1:
                            item.strength -= 1
                        # delete brick
                        else:
                            item.rect = (0, 0, 0, 0)
                    if abs(self.rect.top - item.bottom) < diff_between and self.speed_y < 0:
                        self.speed_y *= -1
                        if item.strength > 1:
                            item.strength -= 1
                        else:
                            item.rect = (0, 0, 0, 0)
                    if abs(self.rect.right - item.left) < diff_between and self.speed_x > 0:
                        self.speed_x *= -1
                        if item.strength > 1:
                            item.strength -= 1
                        else:
                            item.rect = (0, 0, 0, 0)
                    if abs(self.rect.left - item.right) < diff_between and self.speed_x < 0:
                        self.speed_x *= -1
                        if item.strength > 1:
                            item.strength -= 1
                        else:
                            item.rect = (0, 0, 0, 0)
                # if a bricks was found then the wall is not destroyed - the game continuous
                if item.rect != (0, 0, 0, 0):
                    wall_destroyed = False

        # if no bricks was found then the wall is destroyed and a player won
        if wall_destroyed:
            self.game = 1

        # moving the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game


current_paddle = paddle()
current_ball = ball(current_paddle.x + (current_paddle.width / 2), current_paddle.y - current_paddle.height)


def main_menu():
    """
    Window that allows level selection using buttons
    """
    run = True
    click = False
    while run:
        screen.blit(bg_img, (0, 0))
        x, y = pygame.mouse.get_pos()
        font = pygame.font.SysFont('Times New Roman', 60)
        button_1 = pygame.Rect(100, 280, 400, 100)
        button_2 = pygame.Rect(100, 460, 400, 100)
        pygame.draw.rect(screen, color3, button_1, 0, 5)
        pygame.draw.rect(screen, color3, button_2, 0, 5)

        draw_text('WELCOME TO', font, (255, 255, 255), screen, 100, 20)
        draw_text('ARKANOID', font, (255, 255, 255), screen, 135, 80)
        draw_text('SELECT LEVEL', font, (255, 255, 255), screen, 90, 200)
        draw_text('EASY', font, (255, 255, 255), screen, 220, 295)
        draw_text('HARD', font, (255, 255, 255), screen, 220, 475)
        # buttons to select difficulty level
        if button_1.collidepoint((x, y)):
            if click:
                game(1)
        if button_2.collidepoint((x, y)):
            if click:
                game(2)

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def gameover_menu(status: int, time_cur: str) -> None:
    """
    Final menu with stats and restart button.

    :param status: Win or lose condition,
    :param time_cur: String with formated time
    :return: None
    """
    try:
        time_str = time_cur.split(':')
        if len(time_str) != 3:
            raise ValueError('Invalid time string')
        hours, minutes, seconds = map(int, time_str)
        if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
            raise ValueError('Invalid time string')
    except ValueError as e:
        raise ValueError(f"Invalid time string '{time_cur}': {str(e)}")

    run = True
    click = False
    while run:
        screen.blit(bg_img, (0, 0))
        x, y = pygame.mouse.get_pos()
        font = pygame.font.SysFont('Times New Roman', 60)

        if status == 1:
            draw_text('YOU WON!', font, (255, 255, 255), screen, 160, 60)
        elif status == -1:
            draw_text('YOU LOST!', font, (255, 255, 255), screen, 150, 60)

        draw_text('TIME USED:', font, (255, 255, 255), screen, 145, 200)
        draw_text(str(time_cur), font, (255, 255, 255), screen, 245, 270)

        # create a button to restart
        button_1 = pygame.Rect(100, 460, 400, 100)
        pygame.draw.rect(screen, color3, button_1, 0, 5)
        draw_text('RESTART', font, (255, 255, 255), screen, 170, 475)

        # if clicked then restart a program
        if button_1.collidepoint((x, y)):
            if click:
                main_menu()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def game(level: int) -> None:
    """
    Active game mode.

    :param level: Easy(1) or Hard (2) level of the game
    :return: None
    """
    if level not in [1, 2]:
        raise ValueError("Invalid level provided. Level must be 1 (Easy) or 2 (Hard).")

    # initialise ball movement permission
    active_ball = False

    # initialise brickwall
    wall = brick_wall(level)
    wall.create_wall()

    run = True

    # start stopwatch
    start_time = time.time()
    while run:
        screen.blit(bg_img, (0, 0))

        # draw a wall, a paddle and a ball
        wall.draw_wall()
        current_paddle.draw()
        current_ball.draw()

        # ball moves
        if active_ball:
            current_paddle.move()
            # check if the wall is destroyed or the ball fell down
            active_game = current_ball.move(wall)

            # if the wall is destroyed or the ball fell down
            if active_game != 0:
                # block ball moves
                active_ball = False

                # reset all the object on their default positions
                ball.default(current_ball, current_paddle.x + (current_paddle.width / 2),
                             current_paddle.y - current_paddle.height)
                paddle.default(current_paddle)
                wall.create_wall()

                # stop stopwatch
                end_time = time.time()
                current_time = time_convert(end_time - start_time)
                gameover_menu(active_game, current_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not active_ball:
                active_ball = True

        pygame.display.update()


main_menu()
pygame.quit()
