import pygame
from pygame.locals import *
import random

class DanceSpotlight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("placeholder_assets/Sprout Lands - Sprites - Basic pack/Objects/Egg_item.png")
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect() #creates hitbox with image dimensions
        self.rect.center = (320, 240)

    def spawn(self):
        self.rect.center = (random.uniform(30, 610), 240)