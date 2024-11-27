import pygame
from pygame.locals import *
import random

class DanceSpotlight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("art/spotlight_sprite.PNG")
        # self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect() #creates hitbox with image dimensions
        self.rect.center = (320, 340)

    def spawn(self):
        self.rect.center = (random.uniform(30, 610), 340)