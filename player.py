import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer):
        super().__init__(group)
        
        self.import_assets()
        self.status = "down"
        self.frame_index = 0
        
        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
        # vector z is layer of images
        self.z = LAYERS["main"]
    
        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        
        # collision
        self.collision_sprites = collision_sprites
        # set collision boundry
        self.hitbox = self.rect.copy().inflate((-126, -70))
        
        #tools
        self.selected_tool = "hoe"
        
        # timers
        # so when type key in a period of time only change once
        self.timers = {
            "tool using": Timer(350, self.use_tool),
            "tool switching": Timer(200),
            "seed using": Timer(350, self.use_seed),
            "seed switching": Timer(200)
        } 
        
        # tools
        self.tools = ["hoe", "water", "hand"]
        self.tools_index = 0
        self.selected_tool = self.tools[self.tools_index]
        
        # seeds
        self.seeds = ["corn", "tomato"]
        self.seeds_index = 0
        self.selected_seed = self.seeds[self.seeds_index]
        
        # inventory
        self.item_inventory ={
            "golden apple" : 0,
            "red apple" : 0,
            "corn" : 0,
            "tomato" :0
        }
        
        
        # interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        
    def use_tool(self):
        if self.selected_tool == "hoe":
            self.soil_layer.get_hit(self.target_pos)
            
        if self.selected_tool == "hand":
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.pick()
        
        if self.selected_tool == "water":
            self.soil_layer.water(self.target_pos)
        
    def get_target_pos(self):
        
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
     
    def use_seed(self):
        pass
    
    def import_assets(self):
        self.animations = {"up" : [], "down": [], "left": [], "right": [], 
                           "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
                           "right_hoe": [], "left_hoe": [], "up_hoe": [], "down_hoe": [],
                           "right_water": [], "left_water": [], "up_water": [], "down_water": []}
        
        for animation in self.animations.keys():
            full_path = "assets/graphics/character" + "/" + animation
            self.animations[animation] = import_folder(full_path)
           
    def animate(self, dt):  
        
        self.frame_index += 6 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
                
        self.image = self.animations[self.status][int(self.frame_index)]
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if not self.timers["tool using"].active and not self.sleep:
            #directions
            if keys[pygame.K_UP]:
                self.direction.y = -1 #change sprite pics
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down" 
            else:
                self.direction.y = 0
            
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right" 
            else:
                self.direction.x = 0
                
            #tool use
            if keys[pygame.K_j]:
                self.timers["tool using"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                
            #change tools by key q
            if keys[pygame.K_q] and not self.timers["tool switching"].active:
                self.timers["tool switching"].activate()
                self.tools_index += 1
                self.tools_index = self.tools_index % len(self.tools)
                self.selected_tool = self.tools[self.tools_index]
            
            #seeds use
            if keys[pygame.K_k]:
                self.timers["seed using"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                
            #change seeds
            if keys[pygame.K_e] and not self.timers["seed switching"].active:
                self.timers["seed switching"].activate()
                self.seeds_index += 1
                self.seeds_index = self.seeds_index % len(self.seeds)
                self.selected_seed = self.seeds[self.seeds_index]
                
            if keys[pygame.K_SPACE]:
                collided_inter_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_inter_sprite:
                    if collided_inter_sprite[0].name == "Trader":
                        pass
                    else:
                        self.sleep = True
                        self.status = "down_idle"                       
                          
    def get_status(self):
        # idle pic
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + "_idle"
        # tool pic
        if self.timers["tool using"].active:
            if self.selected_tool == "hand":
                self.status = self.status.split('_')[0] + "_idle"
            else:
                self.status = self.status.split('_')[0] + '_' + self.selected_tool
        
    def move(self, dt):
        # normalize the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            # horizontal
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = round(self.pos.x)
            self.collision("horizontal")
            
            # vertical
            self.pos.y += self.direction.y * self.speed * dt
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = round(self.pos.y)
            self.collision("vertical")
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox"):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                        
                    if direction == "vertical":
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
            
    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        
        self.move(dt)
        self.animate(dt)
        