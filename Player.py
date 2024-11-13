import pygame
from pygame.locals import *

# player class inherits from pygame.sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, resolution, sprite_groups):
        super().__init__()
        #TODO: change sprite image
        self.resolution = resolution
        # initiate sprite
        self.image = pygame.image.load("placeholder_assets/Sprout Lands - Sprites - Basic pack/Characters/sprite1.png")
        pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect() #creates hitbox with image dimensions
        self.rect.center = (resolution[0]/2, resolution[1]/2) #sprite spawn location

        #add to sprite groups
        for group in sprite_groups:
            group.add(self)

    def move(self, move_speed):
        pressed_keys = pygame.key.get_pressed()

        # move up
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -move_speed)

        # move down
        if self.rect.bottom < self.resolution[1]:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, move_speed)

        #if sprite is not at left edge move left
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-move_speed, 0)

        #move right
        if self.rect.right < self.resolution[0]:       
          if pressed_keys[K_RIGHT]:
              self.rect.move_ip(move_speed, 0)