import pygame
from pygame.locals import *
import random

class ShopItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("placeholder_assets/Sprout Lands - Sprites - Basic pack/Objects/shop_sprite.png")
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect() #creates hitbox with image dimensions
        self.rect.center = (random.uniform(24, 616), 0) #sprite spawn location

    def spawn(self):
        self.rect.center = (random.uniform(24, 616), 0) #sprite spawn location

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > 640:
            self.rect.center = (random.randint(24, 616), 0)