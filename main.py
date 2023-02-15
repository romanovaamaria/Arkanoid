import pygame

pygame.init()

screen_width = 500
screen_height = 500

# setting screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arkanoid')

# setting background image
bg_img = pygame.image.load('backgr.jpg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

run = True
while run:
    screen.blit(bg_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
