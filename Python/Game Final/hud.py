import pygame
from settings import *

#TIMER
class HUD():
    
    def __init__(self, width, height):
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        
        self.width = width
        self.height = height
        
        self.hud_color = (25, 200, 100, 255)
        
        self.items_surface = pygame.Surface((width, height * 0.06), pygame.SRCALPHA)
        self.items_surface.fill(self.hud_color)
        
        self.render_pos = [self.width - 10, 10]
        
        self.images = self.load_images()
        
        self.display_surf = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bar_rect = pygame.Rect(10,10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        #self.coin_img = self.scale_images(self.images["coin"])
            
    
    def draw(self, screen, player):
        screen.blit(self.items_surface, (0,0))
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        screen.blit(self.images["coin"], (200,-30))
        text = self.my_font.render("X" + str(player.getInventory().getCoins()), False, (0,0,0))
        screen.blit(text, (270, 0))
        
    def load_images(self):
        coin = pygame.image.load("0.8\\graphics\\particles\\nova\\0.png")
        coin = pygame.transform.scale(coin, (100,100))
        
        images = {
            "coin": coin,
        }
        
        return images
        
    def scale_images(self, img, w=0, h=0):
        if (w==0 and h == 0):
            pass
        elif h == 0:
            scale = w / img.get_width()
            h = scale * img.get_height()
            img = pygame.transform.scale(img, int(w), int(h))
        elif w == 0:
            scale = h / img.get_height()
            w = scale * img.get_width()
            img = pygame.transform.scale(img, int(w), int(h))
        else:
            img = pygame.transform.scale(img, int(w), int(h))
            
        return img
    
    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surf, UI_BG_COLOR, bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        pygame.draw.rect(self.display_surf, color, current_rect)
        pygame.draw.rect(self.display_surf, UI_BORDER_COLOR, bg_rect, 3)