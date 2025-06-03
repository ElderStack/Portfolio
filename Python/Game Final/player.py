import pygame
from settings import *
from debug import debug
from pygame import mixer
from moving_parent import Moving_Parent
from inventory import Inventory
from support import import_folder

class Player(Moving_Parent):
    def __init__(self, pos, groups, obstacle_sprites, inv):
        super().__init__(pos, groups, obstacle_sprites, '0.8\\graphics\\player\\down_idle\\idle_down.png', 15)
        
        
        self.character_path = "0.8\\graphics\\player\\"
        #player stats
        self.stats = {'health': 100,
                        'x_speed': 10,
                        'x_accel':1.2,
                        'x_decel':0.5,
                        'x_air_speed': 0,
                        'y_speed': 20,
                        'wall_jump_x': 30,
                        'wall_jump_y': -15,
                        'jump_accel': -18.5,
                        'coyote_frames': 5,
                        'dash_speed': 40,
                        'dash_length': 10,
                        'dash_cooldown': 500,
                        'wall_jump_cooldown': 200,
                        }
        
        self.health = self.stats['health']
        
        #animation vars
        self.animations = {}
        self.importPlayerAssets()
        self.status = 'right'
        self.frame_index = 0
        self.animation_speed = 0.15
        
        #movement variables (pixels per frame)
        #constants
        self.X_ACCEL_AMT = self.stats['x_accel']
        self.X_DECEL_AMT = self.stats['x_decel']
        self.GRAVITY_DEFAULT = .9
        
        #x-direction variables
        self.x_max_speed = self.stats['x_speed']
        self.x_change = 0
        self.x_accel = 0

        #x_max_speed switches between these two based on state of player
        self.x_max_air_speed = self.x_max_speed + self.stats['x_air_speed']
        self.x_max_ground_speed = self.stats['x_speed']
        
        #y-direction variables
        self.y_max_speed = self.stats['y_speed']
        self.y_change = 0
        self.y_accel = 0
        
        self.can_dash = False
        self.dash_speed = self.stats['dash_speed']
        self.dash_length = self.stats['dash_length']
        self.dashing_left = False
        self.dashing_right = False
        self.dash_time = 0
        self.dash_frame_counter = 0
        self.dash_cooldown = self.stats['dash_cooldown']
        
        #jump vars
        self.jump_accel = self.stats['jump_accel']
        
        #wall vars
        self.touching_wall = False
        self.touching_ground = False
        self.touching_left = False
        self.touching_right = False
        
        self.wall_jump_x_change = self.stats['wall_jump_x']
        self.wall_jump_y_change = self.stats['wall_jump_y']
        self.coyote_time = self.stats['coyote_frames']
        self.frames_since_ground = 0
        self.wall_jump_cooldown = self.stats['wall_jump_cooldown']
        self.wall_jump_frame = 0
        
        self.inventory = inv
        
        self.joystick = 0
        
        self.can_left = True
        self.can_right = True
        
        

    def setup(self, pos, group, obs, inv):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.add(group)
        self.obstacle_sprites = (obs)
        self.inventory = inv

    def importPlayerAssets(self):
        #print(self.character_path)
        self.animations = {'left': [],
                            'right': [],
                            'right_idle': [],
                            'left_idle': [],}
                
        for animation in self.animations.keys():
            full_path = self.character_path + animation
            self.animations[animation] = import_folder(full_path)
            for i in range(len(self.animations[animation])):
                self.animations[animation][i] = pygame.transform.scale(self.animations[animation][i], (100,100))

    def cooldowns(self):
        self.current_time = pygame.time.get_ticks()
        
        if self.dash_frame_counter > self.dash_length:
            self.dashing_left = False
            self.dashing_right = False
            self.dash_frame_counter = 0
        
        if self.wall_jump_frame > self.wall_jump_cooldown:
            self.can_left = True
            self.can_right = True
            #math for wall_jump_frame
        
    def getStatus(self):
        if self.x_change > 0:
            self.status = 'right'
        
        if self.x_change < 0:
            self.status = 'left'
            
        if self.status == 'right' and self.x_change == 0:
            self.status = 'right_idle'
            
        if self.status == 'left' and self.x_change == 0:
            self.status = 'left_idle'    

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        if len(animation) != 0:
            self.image = animation[int(self.frame_index)]
            
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def getInventory(self):
        return self.inventory

    #add speed when jump
    #touching wall var reset
    
    """
    Return nothing
    No arguments
    Description: Uses movement vectors from input() to move the player
    """
    def move(self):
        keys = pygame.key.get_pressed()
        # try:
        #     for i in range(16):
        #         if self.joystick.get_button(i):
        #             print(i)
        # except:
        #     pass
        
        """
        A = 0
        B = 1
        X = 2
        Y = 3
        D-PAD R = 14
        D-PAD D = 12
        D-PAD U = 11
        D-PAD L = 13
        BUMPER L = 9
        BUMPER R = 10
        + = 6
        - = 4
        SCREENSHOT = 15
        HOME = 5
        R3 = 8
        L3 = 7
        """
        
        
        #dashing
        if not self.touching_ground:
            #if (self.current_time - self.dash_time > self.dash_cooldown) or  (self.touching_left or self.touching_right):
            if self.touching_left or self.touching_right:
                self.can_dash = True
            # else:
            #     self.can_dash = False
        else:
            if self.current_time - self.dash_time > self.dash_cooldown:
                self.can_dash = True
            else:
                self.can_dash = False
        
        if keys[pygame.K_LSHIFT] and self.can_dash and not self.dashing_left and not self.dashing_right:
            self.dash_time = pygame.time.get_ticks()
            self.can_dash = False
            if self.status == 'right' or self.status == 'right_idle':
                self.dashing_right = True
            elif self.status == 'left' or self.status == 'left_idle':
                self.dashing_left = True
                
        if self.dash_frame_counter <= self.dash_length:
            self.dash_frame_counter += 1
            if self.dashing_left:
                self.x_change = self.dash_speed * -1
            elif self.dashing_right:
                self.x_change = self.dash_speed
        
        #jump on the right wall
        #if jump button and not touching ground and touching right wall and moving downwards            
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.touching_ground and self.touching_right and (self.y_change > 0 or self.y_change == 0):
            self.touching_right = False
            
            self.can_right = False
            self.wall_jump_frame = pygame.time.get_ticks()
            
            self.y_change = self.wall_jump_y_change
            
            self.x_change = -1 * self.wall_jump_x_change
            
        elif (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not self.touching_ground and self.touching_left and (self.y_change > 0 or self.y_change == 0):
            self.touching_left = False
            
            self.can_left = False
            self.wall_jump_frame = pygame.time.get_ticks()
            
            self.y_change = self.wall_jump_y_change
            
            self.x_change = self.wall_jump_x_change
            
        #jump on ground
        elif (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.touching_ground:
            # self.inventory.increaseCoins()
            self.touching_ground = False
            self.frames_since_ground = self.coyote_time
            
            self.y_accel = self.jump_accel
            # print(self.y_accel)
            
            if self.dashing_right:
                self.x_change += 10
            elif self.dashing_left:
                self.x_change -= 10
            
            if abs(self.x_change) == self.x_max_speed:
                self.y_accel += -3
        
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_max_speed = 30
            self.y_accel = 1
            
        #no verticle direction
        else:
            self.y_accel = 0
            self.y_max_speed = 20
            
            #wallslid
            if self.touching_left or self.touching_right:
                self.y_max_speed = 7
                
            else:
                self.y_max_speed = 20
        
        #right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.can_right:
            self.x_accel = self.X_ACCEL_AMT
            
        #left
        elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.can_left:
            self.x_accel = -1 * self.X_ACCEL_AMT
        
        #nothing
        else:
            #if moving forwards, decel backwards
            if ((self.x_change) > 0):
                self.x_accel = -1 * self.X_DECEL_AMT
                
            elif (self.x_change < 0):
                self.x_accel = self.X_DECEL_AMT
                
            else:
                self.x_accel = 0
        
        #acceleration
        
        #turn around
        if (self.x_change * self.x_accel < 0):
            self.x_accel *= 2
            
        self.x_change += self.x_accel
        self.y_change += self.y_accel + self.GRAVITY_DEFAULT      
        
        #stops moving once player sprite is really slow
        if (abs(self.x_change) < self.X_DECEL_AMT):
            self.x_change = 0
        
        #speed limiters
        if self.touching_ground:
            self.x_max_speed = self.x_max_ground_speed
        else:
            self.x_max_speed = self.x_max_air_speed
        
        if abs(self.x_change) >= self.x_max_speed and not self.dashing_left and not self.dashing_right:
            self.x_change = ( (self.x_change) / abs(self.x_change) ) * self.x_max_speed
        
        if self.y_change >= self.y_max_speed:
            self.y_change = ( (self.y_change) / abs(self.y_change) ) * self.y_max_speed
        
        self.getStatus()
        self.rect.y += self.y_change                    
        self.animate()
        self.collision(False)
        self.rect.x += self.x_change
        self.collision(True)

        debug((self.can_left, self.can_right), 400, 400)
    """
    Returns Nothing
    Arguements: Direction to check collision (String direction)
    Description: Checks collision for player
    """
    def collision(self, direction):
        #direction true is x direction
        if direction:
            #print('coll x')
            touched_right_this_frame = False
            touched_left_this_frame = False
            for sprite in self.obstacle_sprites:
                
                #[tile1, tile2, tile3]
                if sprite.rect.colliderect(self.rect):
                    
                    if self.x_change > 0: #moving right
                        #print("Right")
                        self.rect.right = sprite.rect.left
                        touched_right_this_frame = True
                        
                    if self.x_change < 0: #moving left
                        #print("Left")
                        self.rect.left = sprite.rect.right
                        touched_left_this_frame = True
                        
                    self.x_change = 0
                    
            if touched_left_this_frame:
                self.touching_left = True
            else:
                self.touching_left = False
            
            if touched_right_this_frame:
                self.touching_right = True
            else:
                self.touching_right = False
        
        else:
            touched_ground_this_frame = False
            
            for sprite in self.obstacle_sprites:
                
                if sprite.rect.colliderect(self.rect):
                    
                    if self.y_change > 0: #moving down
                        #print("Down")
                        self.rect.bottom = sprite.rect.top
                        #print('ground coll')
                        touched_ground_this_frame = True
                        
                        if sprite.get_move():
                            self.rect.left += sprite.get_x_change() * 2
                            #print("plat: " + str(sprite.get_x_change()) + ", Player coord: " + str(self.rect.left))
                        
                    if self.y_change < 0: #moving up
                        #print("Up")
                        self.rect.top = sprite.rect.bottom
                        
                    self.y_change = 0
                    
            if touched_ground_this_frame:
                self.touching_ground = True
                self.frames_since_ground = 0
            else:
                self.frames_since_ground += 1
                if (self.frames_since_ground < self.coyote_time):
                    self.touching_ground = True
                else:
                    self.touching_ground = False
        