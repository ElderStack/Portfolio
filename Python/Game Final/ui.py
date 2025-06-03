import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        self.health_bar_rect = pygame.Rect(10,10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        
    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        pygame.draw.rect(self.display_surf, color, current_rect)
        pygame.draw.rect(self.display_surf, UI_BORDER_COLOR, bg_rect, 3)
        
    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)