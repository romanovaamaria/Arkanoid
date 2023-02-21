import pygame
import random as rand
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

cols = 6
rows = 6
class paddle():
    def __init__(self):
        self.default()

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect, 0, 5)
                        
    def default(self):
        #define paddle variables
        self.height = 30
        self.width = int(screen_width*paddle_size / 3)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.rect = Rect(self.x, self.y, self.width, self.height)


    def move(self):

        pos = pygame.mouse.get_pos()  
        x = pos[0]-self.width/2
        if (x>=0) and (x<=(screen_width-100 - self.width/2)):
            self.rect.x = x


class brick():
    def __init__(self, col, row, strength):
        self.col = col
        self.row = row
        self.strength = strength
        self.height = 50
        self.width = screen_width/cols
        self.rect = Rect(self.col*self.width, self.row*self.heigth, self.width, self.height)

class brick_wall():
	def __init__(self, level):
		self.level = level

	def create_wall(self):
		self.rows_of_bricks = []
		for row in range(rows):
			#reset the block row list
			bricks = []
			for col in range(cols):
				block_x = col * self.width
				block_y = row * self.height
				rect = pygame.Rect(block_x, block_y, self.width, self.height)
				if  self.level == 1:              
					strength = 1
				else:
					strength = rand.randint(1, 3)
				current_brick = brick(col,row,strength)
				bricks.append(current_brick)
			self.rows_of_bricks.append(bricks)


current_paddle = paddle()
run = True
while run:
    screen.blit(bg_img, (0, 0))
    current_paddle.draw()
    current_paddle.move()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()
pygame.quit()


