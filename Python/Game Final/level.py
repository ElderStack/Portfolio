import pygame
from settings import *
from tile import Tile
from player import Player
from pygame import mixer
from biden_blast import Biden
from moving_platform import Moving_Platform
from enemy import Enemy
from coin import Coin
from hud import HUD
from support import *
import math

class Level():
    def __init__(self, inv):
        #mixer.music.load("C:\\Users\\jse54\\Desktop\\Code\\Platformer\\Platformer-Game\\I did (not) mean to blow your mind - Copy.mp3")
        #mixer.music.set_volume(.075)
        #mixer.music.play(-1)
                
        self.moving_tiles = []
        self.coins = []
        self.moving_speeds = [10, 10, 10]
        self.moving_width = [50, 50, 50]
        self.horizontal = [True, True, True]
        
        #get the disp surf
        self.display_surface = pygame.display.get_surface()
        
        #sprite grouping
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.death_sprites = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        self.finish_sprites = pygame.sprite.Group()
        
        self.spike_image = pygame.image.load("0.8\\graphics\\particles\\flame\\frames\\05.png").convert_alpha()
        self.finish_image = pygame.image.load("0.8\\graphics\\biden_blast.jpg").convert_alpha()
        
        self.map_ground_csv = "0.8\\maps\\game._ground.csv"
        
        self.hud = HUD(WIDTH, HEIGHT)
        
        self.inv = inv
        self.player = Player((0,0), [], self.obstacle_sprites, inv)
        
        self.level2_unl = False
        self.level3_unl = False
        
        self.create_map()
    
    def create_map(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.death_sprites = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        self.finish_sprites = pygame.sprite.Group()
        self.player.health = self.player.stats['health']
        
        layout = {
            'ground': import_csv_layout(self.map_ground_csv),
            'enemy': import_csv_layout("0.8\\maps\\game._enemies.csv"),
            'objects': import_csv_layout("0.8\\maps\\game._objects.csv")
        }
        
        #make this work
        graphics = {
            'cliff_tileset':load_spritesheet_image('0.8\\graphics\\tilemap\\[64x64] Rocky Grass.png', 64, 64, (0,0,0)),
            'purple_dungeon_tileset':load_spritesheet_image("0.8\\graphics\\tilemap\\[64x64] Dungeon Bricks Plain.png", 64, 64, (0,0,0)),
            'decorations':load_spritesheet_image("0.8\\graphics\\tilemap\\[64x64] Decoraciones V1.png", 64, 64, (0,0,0))
        }
        
        counter = 0
        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    col = int(col)
                    if col != -1:
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        current_map = graphics['cliff_tileset']
                        
                        #loading tiles
                        if style == 'ground':
                            if col == 395: #death plane tile
                                Tile((x,y), [self.death_sprites, self.visible_sprites], 'death_plane', self.spike_image)
                            elif col == 100: #player
                                #self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites, self.inv)
                                self.player.setup((x,y), self.visible_sprites, self.obstacle_sprites, self.inv)
                            elif col == 200:
                                Tile((x,y), [self.visible_sprites, self.finish_sprites], 'finish', self.finish_image)
                            else:
                                Tile((x,y), [self.obstacle_sprites, self.visible_sprites], 'ground', current_map[col])
                                
                        current_map = graphics['decorations']
                        if style == 'objects':
                            offset = (x + (17 * 64), y + (-2 * 64))
                            if col < 0:
                                col = 0
                            
                            if col == 100:
                                Coin(offset, [self.visible_sprites], self.visible_sprites, self.player)
                            else:
                                Tile(offset, [self.visible_sprites], 'deco', current_map[col])
                            
                        if style == 'enemy':
                            if col != 0:
                                Enemy((x,y), [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites, self.visible_sprites, self.player)
                            
        
    def getPlayer(self):
        return self.player
    
    def getHUD(self):
        return self.hud
    
    def get_unlocks(self):
        return [self.level2_unl, self.level3_unl]
    
    def run(self):
        #updating and drawing the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        
        self.hud.draw(self.display_surface, self.player)
        
        #moving platforms
        for i in range(len(self.moving_tiles)):
            platform = self.moving_tiles[i]
            platform.move(self.moving_speeds[i], self.moving_width[i], self.horizontal[i])
        
        for i in self.finish_sprites:
            if i.rect.colliderect(self.player.rect):
                if self.map_ground_csv == "0.8\\maps\\game._ground.csv":
                    self.level2_unl = True
                    #print("level 2 unlocked")
                elif self.map_ground_csv == "0.8\\maps\\level2.csv":
                    self.level3_unl = True
                    #print("level 3 unlocked")
        
        for i in self.death_sprites:
            if i.rect.colliderect(self.player.rect):
                print("You died")
                self.create_map()
        
        print("player health: " + str(self.player.health))
        if self.player.health <= 0:
            print("You died")
            self.create_map()
                
        for i in range(len(self.collectables)):
            if self.collectables[i].rect.colliderect(self.player.rect):
                self.player.inventory.increaseCoins()
                self.collectables.remove(self.collectables[i])
                break

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        
        self.display_surface = pygame.display.get_surface()
        
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        
        self.offset = pygame.math.Vector2()
        
        self.background = pygame.image.load("0.8\\graphics\\tilemap\\1 Tiles\\IndustrialTile_02.png").convert_alpha()
        #self.floor_surf = pygame.image.load("0.8\\graphics\\tilemap\\2 Background\\plinK.jpg").convert_alpha()
        
    def tileBackground(self, screen, image, player) -> None:
        imageWidth, imageHeight = image.get_size()
        
        # Calculate how many tiles we need to draw in x axis and y axis
        tilesX = math.ceil(100)
        tilesY = math.ceil(40)
        
        self.background_rect = self.background.get_rect(topleft = (0 + (player.rect.centerx // 2) , -500 + (player.rect.centery // 2)))
        
        # Loop over both and blit accordingly
        for x in range(tilesX):
            for y in range(tilesY):
                background_offset_pos = self.background_rect.topleft - self.offset
                screen.blit(image, (x * imageWidth + background_offset_pos.x, y * imageHeight + background_offset_pos.y))
        
    #go through with students
    def custom_draw(self, player):
        
        #getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        self.tileBackground(self.display_surface, self.background, player)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)