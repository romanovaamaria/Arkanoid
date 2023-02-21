import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 700
paddle_size = 1
paddle_color = (224, 187, 228)
# setting screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arkanoid')

# setting background image
bg_img = pygame.image.load('backgr.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

columns = 5
rows = 5


class brick:
    def __init__(self, strength):
        self.width = screen_width // columns
        self.height = 50
        self.strength = strength


class paddle:
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


class ball:
    def __init__(self, x, y):
        self.ball_radius = 14
        self.x = x - self.ball_radius
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 1
        self.speed_y = -1
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

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game




current_paddle = paddle()
current_ball = ball(current_paddle.x + (current_paddle.width / 2), current_paddle.y - current_paddle.height)

run = True
while run:
    screen.blit(bg_img, (0, 0))
    current_paddle.draw()
    current_paddle.move()

    current_ball.draw()
    current_ball.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()
pygame.quit()
