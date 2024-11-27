import pygame
from pygame import *

class Scene():
    def __init__(self, resolution, image):
        self.resolution = resolution
        # initiate sprite
        self.background = pygame.image.load(image)
        # self.background = pygame.transform.scale(self.background, resolution)
