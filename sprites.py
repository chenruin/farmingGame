import pygame
from settings import *
from random import *
from timer import Timer
from pytmx.util_pygame import load_pygame

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS["main"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.2, -self.rect.height * 0.80))
  
class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name
      
class Water(Generic):
    def __init__(self, pos, frames, groups, z):
        self.frames = frames
        self.frame_index = 0
 
        # sprite setup
        super().__init__(
            pos = pos, 
            surf = self.frames[self.frame_index], 
            groups = groups,
            z = LAYERS["water"])
        
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        self.image = self.frames[int(self.frame_index)]
        
    def update(self, dt):
        self.animate(dt)
        
class Flower(Generic):
    def __init__(self, pos, surf, groups, z=LAYERS["main"]):
        super().__init__(pos, surf, groups, z)
        self.hitbox = self.rect.copy().inflate((-20, -self.rect.height * 0.95))
    
class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        #fruits
        self.apple_images = {
        "red": "assets/graphics/fruit/Apple Red.png",
        "golden": "assets/graphics/fruit/GoldenApple.png",
        }
        #self.apple_surf = pygame.image.load(self.apple_images["red"])
        self.apple_pos = FRUITS_POS["RED APPLE"]
        #self.appleG_surf = pygame.image.load(apple_images["golden"])
        #self.appleG_pos = FRUITS_POS["GOLDEN APPLE"]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()
               
        self.player_add = player_add
        
    def pick(self):
        
        # remove fruits
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            self.player_add("apple")
            random_apple.kill()
        
    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 20) < 5:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                apple_type = "red"
                
                Generic(
                    pos = (x, y), 
                    surf=pygame.image.load(self.apple_images[apple_type]),
                    groups=[self.apple_sprites, self.groups()[0]],
                    z = LAYERS["fruit"])
            
            elif randint(0,30) == 22:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                apple_type = "golden" 
            
                Generic(
                    pos = (x, y), 
                    surf = pygame.image.load(self.apple_images[apple_type]),
                    groups=[self.apple_sprites, self.groups()[0]],
                    z = LAYERS["fruit"])
                
class SoilLayer:
    def __init__(self, all_sprites):
        
        #
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        
        self.soil_surf = pygame.image.load("assets/graphics/soil/o.png")
        
    def create_soil_grid(self):
        
        ground = pygame.image.load("assets/graphics/world/ground.png")
        # horizontal and vertical tiles
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE
        
        self.grid = [[] for col in range(h_tiles) for row in range(v_tiles)]
        for x, y, _ in load_pygame("assets/data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append('F')
            print(self.grid)
