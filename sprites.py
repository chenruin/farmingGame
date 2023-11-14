import pygame
from pygame.sprite import Group
from settings import *
from random import *
from timer import Timer
from pytmx.util_pygame import load_pygame
from support import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS["main"], fruit_type = None):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate((-self.rect.width * 0.2, -self.rect.height * 0.80))
        self.fruit_type = fruit_type
        
class Interaction(Generic):
    def __init__(self, pos, size, groups, name, fruit_type):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups, fruit_type)
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
        self.fruit_images = {
        "red apple": "assets/graphics/fruit/Apple Red.png",
        "golden apple": "assets/graphics/fruit/GoldenApple.png",
        }
        
        self.apple_pos = FRUITS_POS["apple"]
        self.apple_sprites = pygame.sprite.Group()
        self.name = name
        self.create_fruit()      
        
        self.player_add = player_add
        
    def pick(self):    
        # remove fruits
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            print(random_apple)
            
            fruit = random_apple.fruit_type
        
            self.player_add(fruit)
            #test pos
            print(random_apple.rect.topleft)            
            random_apple.kill()
                    
    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0, 99) < 10:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                fruit_type = "red apple"
                
                Generic(
                    pos = (x, y), 
                    surf=pygame.image.load(self.fruit_images[fruit_type]),
                    groups=[self.apple_sprites, self.groups()[0]],
                    z = LAYERS["fruit"],
                    fruit_type= fruit_type)
            
            elif randint(0, 99) > 97 :
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                fruit_type = "golden apple"
            
                Generic(
                    pos = (x, y), 
                    surf = pygame.image.load(self.fruit_images[fruit_type]),
                    groups=[self.apple_sprites, self.groups()[0]],
                    z = LAYERS["fruit"],
                    fruit_type= fruit_type)

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["soil"]
        
class WaterTile(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = LAYERS['soil water']

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f"assets/graphics/fruit/{plant_type}")
        print("Number of frames:", len(self.frames))  
        print(f"Path: assets/graphics/fruit/{plant_type}")  
        self.soil = soil
        self.check_watered = check_watered
        
        self.stage = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        
        # sprite set
        self.image = self.frames[self.stage]
        print(f"Initial image: {self.image}")  
        print(f"Initial stage: {self.stage}")
        self.y_offset = -16 if plant_type == "corn" else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS["ground plant"]
        
    def grow(self):
        if self.check_watered(self.rect.center):
            self.stage += self.grow_speed
            new_index = int(self.stage)
            print(f"New index: {new_index}")
            self.image = self.frames[int(self.stage)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom +pygame.math.Vector2(0, self.y_offset))
                   
class SoilLayer:
    def __init__(self, all_sprites):
        
        #
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()
        
        self.soil_surf = pygame.image.load("assets/graphics/soil/o.png")
        self.water_surf = pygame.image.load("assets/graphics/soil_water/watered soil.png")
        
        self.create_soil_grid()
        self.create_hit_rects()
        
    def create_soil_grid(self):
        
        ground = pygame.image.load("assets/graphics/world/ground.png")
        # horizontal and vertical tiles
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE
        
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame("assets/data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append('F')
            
    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)
                    
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                
                # the soil is tamed
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    
                    self.create_soil_tiles()
                                    
    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:    
                    SoilTile(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE), 
                        surf=self.soil_surf, 
                        groups=[self.all_sprites, self.soil_sprites])
                    
    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')
                
                pos = soil_sprite.rect.topleft
                surf = self.water_surf
                WaterTile(pos, surf, [self.all_sprites, self.water_sprites])
                
                
    def remove_water(self):
        #remove water sprite
        for sprite in self.water_sprites.sprites():
            sprite.kill()
        
        #update the grid    
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')
                    
    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = "W" in cell
        return is_watered
                    
    def plant_seed(self, target_pos, seed):
    
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                
                if "P" not in self.grid[y][x]:
                    self.grid[y][x].append("P")      
                    Plant(seed, [self.all_sprites, self.plant_sprites], soil_sprite, self.check_watered)  
                               
    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()               
        
