import button
from support import import_folder
from settings import *
import pygame

#no double clicks

class Menu():
    def __init__(self) -> None:
        self.menu_state = "main"
        self.unlocked = False
        
        #change buttons after being clicked

        menu_buttons = import_folder("0.8\\graphics\\menu buttons")
        #shop_buttons = import_folder()
        print(len(menu_buttons))
        lvl1 = menu_buttons[0]
        lvl2 = menu_buttons[1]
        lvl3 = menu_buttons[2]
        audio = menu_buttons[3]
        back = menu_buttons[4]
        keys = menu_buttons[5]
        options = menu_buttons[6]
        quit_image = menu_buttons[7]
        resume = menu_buttons[8]
        video = menu_buttons[9]
        play = menu_buttons[10]
        shop = menu_buttons[11]

        middle_width = (WIDTH / 2)
        
        self.paused_background = pygame.image.load('0.8\\graphics\\tilemap\\2 Background\\plinK.jpg')
        self.main_menu_background = pygame.image.load('0.8\\graphics\\tilemap\\2 Background\\baby.jpg')
        
        self.paused_small = pygame.transform.scale(self.paused_background, (1280,720))
        self.main_image_small = pygame.transform.scale(self.main_menu_background, (1280,720))
                
        #main
        self.play_button = button.Button((middle_width - play.get_width() / 2) - 70, 100, play, 3)

        #pause
        self.options_button = button.Button(middle_width - options.get_width() / 2, 300,options)
        self.quit_button = button.Button(middle_width - quit_image.get_width() / 2, 400,quit_image)
        self.resume_button = button.Button(middle_width - resume.get_width() / 2, 200,resume)

        #options
        self.audio_button = button.Button(middle_width - audio.get_width() / 2, 200,audio)
        self.back_button = button.Button(middle_width - back.get_width() / 2, 500,back)
        self.keys_button = button.Button(middle_width- keys.get_width() / 2, 400,keys)
        self.video_button = button.Button(middle_width- video.get_width() / 2, 300,video)
        
        #level
        self.lvl1 = button.Button(middle_width - lvl1.get_width() / 2, 200,lvl1, 3)
        self.lvl2 = button.Button(middle_width - lvl2.get_width() / 2, 300,lvl2, 3)
        self.lvl3 = button.Button(middle_width - lvl3.get_width() / 2, 400,lvl3, 3)
        
        #shop
        self.shop_button = button.Button(100,100, shop)
        
        self.unlocks = []
    
    def drawButtonsPaused(self, screen):
        game_state = 'paused'
        
        screen.blit(self.paused_small, (0,0))
        if self.menu_state == 'main' or self.menu_state == 'levels':
            self.menu_state = 'paused'
            
        if self.menu_state == 'paused':
            if self.options_button.draw(screen):
                self.menu_state = 'options'
            if self.quit_button.draw(screen):
                #update
                game_state = 'main_menu'
                self.menu_state = 'main'
            if self.resume_button.draw(screen):
                game_state = "game"
                
        elif self.menu_state == "options":
            self.audio_button.draw(screen)
            if self.back_button.draw(screen):
                self.menu_state = "paused"
            self.keys_button.draw(screen)
            self.video_button.draw(screen)
                
        return game_state
    
    def drawButtonsMain(self, screen, player, hud):
        #print("main menu")
        game_state = 'main_menu'
        if self.menu_state == "main":
            screen.blit(self.main_image_small, (0,0))
            if self.play_button.draw(screen):
                self.menu_state = 'levels'
            if self.quit_button.draw(screen):
                game_state = 'quit'
            if self.options_button.draw(screen):
                self.menu_state = 'options'
            if self.shop_button.draw(screen):
                self.menu_state = "shop"
                
        elif self.menu_state == "options":
            screen.blit(self.main_image_small, (0,0))
            self.audio_button.draw(screen)
            if self.back_button.draw(screen):
                self.menu_state = "main"
            self.keys_button.draw(screen)
            self.video_button.draw(screen)
        
        elif self.menu_state == "levels":
            screen.blit(self.paused_small, (0,0))
            if self.lvl1.draw(screen):
                game_state = "lvl1"
            if self.lvl2.draw(screen) and self.unlocks[0]:
                game_state = "lvl2"
            if self.lvl3.draw(screen) and self.unlocks[1]:
                game_state = "lvl3"
            if self.back_button.draw(screen):
                self.menu_state = "main"
                
        elif self.menu_state == "shop":
            screen.blit(self.paused_small, (0,0))
            hud.draw(screen, player)
            
            def checkCost(cost, path, unlocked):
                if player.getInventory().getCoins() >= cost or unlocked:
                    player.character_path = path
                    player.importPlayerAssets()
                    player.getInventory().coins -= cost
                    return True
                else:
                    print('not enough coins')
                    return False
            
            
            if self.keys_button.draw(screen):
                cost = 0
                path = '0.8\\graphics\\player\\'
                checkCost(cost, path, True)
                    
            elif self.video_button.draw(screen):
                if self.unlocked:
                    cost = 0
                else:
                    cost = 3
                path = "0.8\\graphics\\skin_1\\"
                self.unlocked = checkCost(cost, path, self.unlocked)
                    
            if self.back_button.draw(screen):
                self.menu_state = 'main'
                
        return game_state