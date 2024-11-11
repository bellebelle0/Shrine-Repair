import sys
import pygame
from pygame.locals import *
from Player import Player

pygame.init()

fps = 60
fps_clock = pygame.time.Clock()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

#TODO: update with proper bg
background = pygame.image.load("pfad\Group Assignment\Shrine-Repair.jpg")

display = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Shrine Repair")

#initiate sprite groups
all_sprites = pygame.sprite.Group()
interactive_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

#initiate sprites
player = Player(RESOLUTION, [all_sprites])

### game update loop ###
while True:
    #quit game 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #draw visuals to display
    display.blit(background, (0,0))
    for sprite in all_sprites:
        display.blit(sprite.image, sprite.rect)

    #update
    player.move(5)
    pygame.display.update()
    fps_clock.tick(fps)