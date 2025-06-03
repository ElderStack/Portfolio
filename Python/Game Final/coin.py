import pygame

class Coin(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, visible_sprites, player):
        super().__init__(groups)
        
        self.image = pygame.image.load("0.8\\graphics\\particles\\nova\\0.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.visible_sprites = visible_sprites
        self.player = player
        
    def collision(self):
        if self.rect.colliderect(self.player.rect):
            self.visible_sprites.remove(self)
            self.player.getInventory().increaseCoins()
            
    def update(self):
        self.collision()