import pygame

class Moving_Parent(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups, obstacle_sprites, image_path, x_max_speed):
        super().__init__(groups)
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.obstacle_sprites = obstacle_sprites
        self.x_max_speed = x_max_speed
        
        self.touching_ground = False
        self.touching_wall = False
        
        self.gravity = 10
        
        self.hitbox = self.rect.inflate(0, -25)
        
        self.stats = {}
        
        
    def move(self):
        pass
    
    def collision(self):
        pass
    
    def cooldowns(self):
        pass
    
    def update(self):
        self.cooldowns()
        self.move()