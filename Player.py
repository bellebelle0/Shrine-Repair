import pygame
from pygame.locals import *

# player class inherits from pygame.sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, resolution, spawn_point, sprite_groups, filepath):
        super().__init__()
        #TODO: change sprite image
        self.resolution = resolution
        # initiate sprite
        self.image = pygame.image.load(filepath)
        self.image = pygame.transform.scale_by(self.image, 0.23)
        self.rect = self.image.get_rect() #creates hitbox with image dimensions
        self.rect.center = spawn_point #sprite spawn location
        self.respawn_point = spawn_point

        #add to sprite groups
        for group in sprite_groups:
            group.add(self)

    #TODO: update for diff modes, all games limited to horizontal movement
    def move(self, move_speed, mode):
        pressed_keys = pygame.key.get_pressed()

        if mode == "home":
            # move up
            if self.rect.top > 210:
                if pressed_keys[K_UP]:
                    self.rect.move_ip(0, -move_speed)

            # move down
            if self.rect.bottom < self.resolution[1]:
                if pressed_keys[K_DOWN]:
                    self.rect.move_ip(0, move_speed)

            #if sprite is not at left edge move left
            if self.rect.left > 84:
                if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-move_speed, 0)

            #move right
            if self.rect.right < self.resolution[0]:       
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(move_speed, 0)

        #TODO: copy and change here for different game modes
        elif mode == "dance game":

            #move left
            if self.rect.left > 0: #if sprite is not at left edge move left
                if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-move_speed, 0)

            #move right
            if self.rect.right < self.resolution[0]:       
                if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(move_speed, 0)

        else:
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

    # reset player position
    def spawn(self):
        self.rect.center = self.respawn_point