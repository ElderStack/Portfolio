import pygame
from settings import *
import math

class Moving_Platform(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
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
        
    def move(self, speed, width, horizontal):
        self.frame_counter += 1
        
        if horizontal:
            self.curr_pos = self.init_x + width * math.sin(self.frame_counter/speed)
            self.next_pos = self.init_x + width * math.sin((self.frame_counter + 1)/speed)
            self.x_change = self.next_pos - self.curr_pos
            self.rect.x = (self.next_pos)
        else:
            self.curr_pos = self.init_y + width * math.sin(self.frame_counter/speed)
            self.next_pos = self.init_y + width * math.sin((self.frame_counter + 1)/speed)
            self.y_change = self.next_pos - self.curr_pos
            self.rect.y = (self.next_pos)
            
    def get_move(self):
        return True
    
    def get_x_change(self):
        return self.x_change