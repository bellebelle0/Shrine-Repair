import sys
import pygame
from pygame.locals import *

#TODO: create multiple scenes for diff rooms
#TODO: object interactions
#TODO: player sprite and class
#TODO: obstacle sprites
#TODO: interactive objects
#TODO: function to initiate all sprites

#initialize pygame engine
pygame.init()

### pygame configurations ###
#refresh rate configs
fps = 60
fps_clock = pygame.time.Clock()


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)

#TODO: update with proper bg
background = pygame.image.load("placeholder_assets/Sky_Paint1.png")

display = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Shrine Repair")
display.blit(background, (0,0))

### game update loop ###
while True:
    #quit game 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps_clock.tick(fps)