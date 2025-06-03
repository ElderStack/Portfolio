import pygame
from settings import *
from moving_parent import Moving_Parent
from debug import debug
from support import import_folder

class Enemy(Moving_Parent):
    def __init__(self, pos, groups, obstacle_sprites, visible_sprites, player):
        super().__init__(pos, groups, obstacle_sprites, '0.8\\graphics\\monsters\\squid\\idle\\0.png', 1)
        self.direction = -1
        self.visible_sprites = visible_sprites
        self.player = player
        
        self.animations = {}
        self.importAssets()
        self.status = "move"
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.attack_cooldown = 600
        self.attack_time = None
        self.damage = 10
        self.attacking = False
        
        
    def importAssets(self):
        character_path = "0.7\\graphics\\monsters\\squid\\"
        self.animations = {'move': [],
                            'idle': [],
                            'attack': []}
                
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            print(current_time - self.attack_time)
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    def getStatus(self):
        self.status = "move"
        
    def animate(self):
        animation = self.animations[self.status]
        
        #loop animation frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
        
    def collision(self, direction):
        player_bottom = self.player.rect.y + self.player.rect.height
        enemy_head = self.rect.y + 10
        
        if direction:
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.x_change > 0:
                        self.rect.right = sprite.rect.left
                        
                    if self.x_change < 0:
                        self.rect.left = sprite.rect.right
                        
                    self.direction *= -1
        
        else:
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.y_change > 0:
                        self.rect.bottom = sprite.rect.top
                        
                    if self.y_change < 0:
                        self.rect.top = sprite.rect.bottom
        
        if self.rect.colliderect(self.player.rect):
            #lowest player point >= top of enemy
            
            if player_bottom < enemy_head:
                
                print("Player bottom: " + str(player_bottom))
                print("Enemy Head: "  + str(enemy_head))
                print("Delete")
                
                self.visible_sprites.remove(self)
                self.player.y_change += -15
            
            else:
                if not self.attacking:
                    self.attack_time = pygame.time.get_ticks()
                    self.player.health -= self.damage
                    self.attacking = True
    
    def move(self):
        self.getStatus()
        self.animate()
        self.y_change = self.gravity
        self.rect.y += self.y_change
        self.collision(False)
        self.x_change = self.x_max_speed * self.direction
        self.rect.x += self.x_change
        self.collision(True)
        
        self.cooldowns()