import pygame
from settings import *

class Biden(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('C:\\Users\\jse54\\Desktop\\Code\\Platformer\\Platformer-Game\\Hour 4\\graphics\\biden_blast.jpg').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)