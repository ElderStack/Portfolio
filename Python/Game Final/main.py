import pygame
import sys
from settings import *
from debug import debug
from level import Level 
from menu import Menu
from inventory import Inventory
import math

class Game():
    
    def __init__(self):
        
        pygame.init()
        # pygame.joystick.init()
        desktop_size = pygame.display.get_desktop_sizes()
        #ww(desktop_size[0][0])
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        #self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("0.8")
        self.clock = pygame.time.Clock()
        self.game_state = 'main_menu'
        self.inventory = Inventory()
        self.menu = Menu()
        self.level = Level(self.inventory)
    
    def run (self): 
        frames = 0
        
        while True:
            self.menu.unlocks = self.level.get_unlocks()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = 'paused'
                        self.menu_state = 'paused'
                        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill((0, 0, 0))
            print(self.game_state)
            if self.game_state == "game":
                self.level.run()
            elif self.game_state == "lvl1":
                # self.level.run() 
                self.level.map_ground_csv = "0.8\\maps\\game._ground.csv"
                self.level.create_map()
                self.game_state = "game"
                
            elif self.game_state == "lvl2":
                #self.level.run() 
                self.level.map_ground_csv = "0.8\\maps\\level2.csv"
                self.level.create_map()
                self.game_state = "game"
                
            elif self.game_state == "lvl3":
                #self.level.run() 
                self.level.map_ground_csv = "0.8\\maps\\level2.csv"
                self.level.create_map()
                self.game_state = "game"
                
            elif self.game_state == 'paused':
                self.game_state = self.menu.drawButtonsPaused(self.screen)
                
            elif self.game_state == 'main_menu':
                self.game_state = self.menu.drawButtonsMain(self.screen, self.level.getPlayer(), self.level.getHUD())
                
            elif self.game_state == 'quit':
                pygame.quit()
                sys.exit()
            
            frames += 1
            pygame.display.update()
            self.clock.tick(FPS)
            pygame.display.set_caption(str(math.ceil(self.clock.get_fps())))

if __name__ == "__main__":
    game = Game()
    game.run()