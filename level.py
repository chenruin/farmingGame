from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from player import *
from overlay import *
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *
#from soil import SoilLayer



class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        #self.player = Player((700,360), self.all_sprites)
        self.tree_sprites = pygame.sprite.Group()
        self.apple_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        
        
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        
        #shop
        #self.menu = Menu(self.player, self.shop)
        self.shop_active = False
        
               
    def setup(self):
        tiled_data = load_pygame("assets/data/map.tmx")
        
        #house floor, layer order matters
        for layer in ["HouseFloor", "HouseFurnitureBottom"]:
            for x, y, surface in tiled_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, LAYERS["house floor"])
        
        #house walls      
        for layer in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surface in tiled_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites)
        
        #fences
        for x, y, surface in tiled_data.get_layer_by_name("Fence").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), surface, [self.all_sprites, self.collision_sprites])
            
        # water
        water_frames = import_folder("assets/graphics/water")
        for x, y, surface in tiled_data.get_layer_by_name("Water").tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites, LAYERS["water"])
        
        # wildflowers, AttributeError: Element has no property tiles
        for flower in tiled_data.get_layer_by_name("Decoration"):
            Flower((flower.x, flower.y), flower.image, [self.all_sprites, self.collision_sprites], LAYERS["main"])
            
        #trees        
        for tree in tiled_data.get_layer_by_name("Trees"):
            Tree((tree.x, tree.y), tree.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], tree.name, self.player_add)
        
        # collisions on map(water, hills)
        for x, y, s in tiled_data.get_layer_by_name("Collision").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
               
        # set player initial location 
        for obj in tiled_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    tree_sprites= self.tree_sprites, 
                    interaction = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    shop = self.shop,)
                
            if obj.name == "Bed":
                Interaction(pos=(obj.x, obj.y),size = (obj.width, obj.height), groups=self.interaction_sprites, name = obj.name, fruit_type= None)
                
            if obj.name == "Trader":
                Interaction(pos=(obj.x, obj.y),size = (obj.width, obj.height), groups=self.interaction_sprites, name = obj.name, fruit_type= None)

        Generic(
            pos = (0,0), 
            surf = pygame.image.load("assets/graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS["ground"])
  
    def player_add(self, item):
        self.player.item_inventory[item] += 1
        ####test
        print(self.player.item_inventory)
 
    def shop(self):
        self.shop_active = not self.shop_active
        
    def reset(self):
        
        # plant grow
        self.soil_layer.update_plants()
        
        # dry up water in soil
        self.soil_layer.remove_water()
        
        # add more apple on the next day
        for tree in self.tree_sprites.sprites():
            for apple in self.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()
 
    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites:
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
                                     
    def run(self, dt):
        self.display_surface.fill("black")
        
        #update
        if self.shop_active:
            #self.menu.update()
            pass
        else:
            self.all_sprites.update(dt)
            self.plant_collision()
        
        
        camera_offset = pygame.math.Vector2(
            SCREEN_WIDTH / 2 - self.player.rect.centerx,
            SCREEN_HEIGHT / 2 - self.player.rect.centery
        )
        
        self.all_sprites.customize_draw(self.display_surface, camera_offset)
                
        self.overlay.display()
                
        if self.player.sleep:
            self.transition.play()
            
        
""" #original code, but the camera didn't work 

        self.display_surface.fill('white')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)
        
        self.overlay.display()
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, sprite.rect)
"""   

class CameraGroup(pygame.sprite.Group):
    def customize_draw(self, display_surface, camera_offset):
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.move(camera_offset)
                    
                    
                    display_surface.blit(sprite.image, offset_rect)
                    
                    
                 