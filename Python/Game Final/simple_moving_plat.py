import pygame
from pygame.sprite import AbstractGroup
from settings import *

class Simple_Plat(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        
        self.image = pygame.image.load('0.7\\graphics\\weapons\\axe\\full.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.frame_counter = 0
        self.init_x = self.rect.x
        self.init_y = self.rect.y
        self.next_pos = 0
        self.curr_pos = 0
        self.x_change = 0
        self.y_change = 0
        self.direction = 1
        
    def move(self, speed, width):
        self.speed = speed
        self.rect.left += speed * self.direction
        if self.rect.left > (width + self.init_y) or self.rect.left < (width - self.init_y):
            self.direction *= -1
            
    def get_move(self):
        return True
    
    def get_x_change(self):
        return self.speed