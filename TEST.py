

import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255, 50)  # This color contains an extra integer. It's the alpha value.
PURPLE = (255, 0, 255)

# screen = pygame.display.set_mode((640, 480))
# screen.set_colorkey((255, 255, 255))
clock = pygame.time.Clock()


size = (50, 50)
red_image = pygame.Surface(size)
green_image = pygame.Surface(size)
blue_image = pygame.Surface(size, pygame.SRCALPHA)  # Contains a flag telling pygame that the Surface is per-pixel alpha
purple_image = pygame.Surface(size)

red_image.set_colorkey(BLACK)
green_image.set_alpha(50)
# For the 'blue_image' it's the alpha value of the color that's been drawn to each pixel that determines transparency.
purple_image.set_colorkey(BLACK)
purple_image.set_alpha(50)

pygame.draw.rect(red_image, RED, red_image.get_rect(), 10)
pygame.draw.rect(green_image, GREEN, green_image.get_rect(), 10)
pygame.draw.rect(blue_image, BLUE, blue_image.get_rect(), 10)
pygame.draw.rect(purple_image, PURPLE, purple_image.get_rect(), 10)

moviex = 75
moviey = 45
screen = pygame.display.set_mode((200, 140))
bg = pygame.image.load('images/bg.bmp') #.set_colorkey((0,0,0))
# bg.set_colorkey((0,0,0, 250))
# bg.set_alpha(1)
# bg.set_alpha(30)
while True:
    clock.tick(60)
    # screen.fill(WHITE)  # Make the background white. Remember that the screen is a Surface!
    # my_surface = my_surface.convert_alpha()
    # screen.fill((0, 255, 0))

    # -----------------------------------------
    screen.blit(bg,(20,0))
    screen.blit(red_image, (moviex, moviey))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moviey -= 3
            elif event.key == pygame.K_s:
                moviey += 3
            elif event.key == pygame.K_a:
                moviex -= 3
            elif event.key == pygame.K_d:
                moviex += 3
            if event.key == pygame.K_ESCAPE:
                quit()

    pygame.display.update()




