import pygame
import random as rand
import argparse
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 700
paddle_size = 1

# default color palette
paddle_color = (224, 187, 228)
color1 =(254, 200, 216)
color2 = (210, 145, 188)
color3= (149, 125, 173)

# setting screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arkanoid')

# setting background image
bg_img = pygame.image.load('backgr.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

columns = 6
rows = 6

click = False

parser = argparse.ArgumentParser()
parser.add_argument('--color', help ='Change color palette', choices =['1','2','3','4'])
args = parser.parse_args()

if args.color == '1':
    paddle_color = (224, 187, 228)
    color1 =(254, 200, 216)
    color2 = (210, 145, 188)
    color3= (149, 125, 173)
elif args.color == '2':
    paddle_color = (247, 226, 203)
    color1 =(250, 214, 165)
    color2 = (247, 179, 156)
    color3= (242, 150, 150)
elif args.color == '3':
    paddle_color = (111, 211, 252)
    color1 =(97, 168, 237)
    color2 = (62, 115, 206)
    color3= (49, 66, 190)
elif args.color == '4':
    paddle_color = (143, 217, 168)
    color1 =(72, 191, 145)
    color2 = (21, 153, 122)
    color3= (1, 121, 111)


def draw_text(str, font, color, screen, x, y):
    text = font.render(str, 1, color)
    textrect = text.get_rect()
    textrect.topleft = (x, y)
    screen.blit(text, textrect)


class paddle():
    def __init__(self):
        self.default()

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect, 0, 5)
                        
    def default(self):
        # define paddle variables
        self.height = 30
        self.width = int(screen_width*paddle_size / 3)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move(self):
        pos = pygame.mouse.get_pos()  
        x = pos[0]-self.width/2
        if (x >= 0) and (x <= (screen_width-100 - self.width/2)):
            self.rect.x = x


class brick():
    def __init__(self, col, row, strength):
        self.col = col
        self.row = row
        self.strength = strength
        self.heigth = 50
        self.width = screen_width/columns
        self.rect = Rect(self.col*self.width, self.row*self.heigth, self.width, self.heigth)


class brick_wall():
    def __init__(self, level):
        self.level = level
    
    def draw_wall(self):
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
        self.rows_of_bricks = []
        for row in range(rows):
            bricks = []
            for col in range(columns):
                if  self.level == 1:
                    strength = 1
                else:
                    strength = rand.randint(1, 3)
                current_brick = brick(col,row,strength)
                bricks.append(current_brick)
            self.rows_of_bricks.append(bricks)


class ball():
    def __init__(self, x, y):
        self.ball_radius = 14
        self.x = x - self.ball_radius
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 1
        self.speed_y = -1
        self.speed_max = 2
        self.game = True

    def draw(self):
        pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius), self.ball_radius)

    def move(self):

        # bounce from the sides and top
        if self.rect.right > screen_width or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1
        # fall at the bottom for game over condition
        if self.rect.bottom > screen_height:
            self.game = False

        # collision with the paddle
        if self.rect.colliderect(current_paddle):
            if abs(self.rect.bottom - current_paddle.rect.top) < 5 and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x *= 1
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x *= -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game


current_paddle = paddle()
current_ball = ball(current_paddle.x + (current_paddle.width/2), current_paddle.y - current_paddle.height)
wall = brick_wall(2)
wall.create_wall()


def main_menu():
    click = False
    while True:
        screen.blit(bg_img, (0, 0))
        x, y = pygame.mouse.get_pos()
        font = pygame.font.SysFont('Times New Roman', 60)
        button_1 = pygame.Rect(100, 260, 400, 100)
        button_2 = pygame.Rect(100, 460, 400, 100)
        if button_1.collidepoint((x, y)):
            if click:
                game(1)
        if button_2.collidepoint((x, y)):
            if click:
                game(2)
        pygame.draw.rect(screen, color3, button_1, 0, 5)
        draw_text('WELCOME TO', font, (255, 255, 255), screen, 50, 20)
        draw_text('ARKANOID', font, (255, 255, 255), screen, 100, 80)
        font = pygame.font.SysFont('Times New Roman', 60)
        draw_text('SELECT LEVEL', font, (255, 255, 255), screen, 100, 200)
        pygame.draw.rect(screen, color3, button_2, 0, 5)
        font = pygame.font.SysFont('Times New Roman', 60)
        draw_text('EASY', font, (255, 255, 255), screen, 200, 280)
        draw_text('HARD', font, (255, 255, 255), screen, 200, 480)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()


def game(level):
     wall = brick_wall(level)
     wall.create_wall()
     run = True
     while run:
        screen.blit(bg_img, (0, 0))
        wall.draw_wall()
        current_paddle.draw()
        current_paddle.move()
        current_ball.draw()
        current_ball.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        pygame.display.update()


main_menu()

pygame.quit()
