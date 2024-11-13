import pygame
from pygame import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, resolution, image, sprite_groups, location):
        super().__init__()
        #TODO: change sprite image
        self.resolution = resolution
        # initiate sprite
        self.image = pygame.image.load(image)
        pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect() #creates hitbox with image dimensions
        self.rect.center = location #sprite spawn location

        #add to sprite groups
        for group in sprite_groups:
            group.add(self)
