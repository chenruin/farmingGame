from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from player import *
from overlay import Overlay
from sprites import *
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        #sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        #self.Player = Player((700,360), self.all_sprites)
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        
        self.setup()
        self.overlay = Overlay(self.Player)
        self.transition = Transition(self.reset, self.Player)
        
           
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
               
        #trees
        for tree in tiled_data.get_layer_by_name("Trees"):
            Tree((tree.x, tree.y),tree.image, [self.all_sprites, self.collision_sprites, self.tree_sprites], tree.name, self.player_add)
        
        # wildflowers, AttributeError: Element has no property tiles
        for flower in tiled_data.get_layer_by_name("Decoration"):
            Flower((flower.x, flower.y), flower.image, [self.all_sprites, self.collision_sprites], LAYERS["main"])
        
        # collisions on map(water, hills)
        for x, y, s in tiled_data.get_layer_by_name("Collision").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
               
        # set player initial location 
        for obj in tiled_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.Player = Player(pos=(obj.x, obj.y), group=self.all_sprites, collision_sprites=self.collision_sprites, tree_sprites= self.tree_sprites, interaction = self.interaction_sprites)
            if obj.name == "Bed":
                Interaction(pos=(obj.x, obj.y),size = (obj.width, obj.height), groups=self.interaction_sprites, name = obj.name)

        Generic(
            pos = (0,0), 
            surf = pygame.image.load("assets/graphics/world/ground.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS["ground"])
  
    def player_add(self, item):
        self.Player.item_inventory[item] += 1
        
    def reset(self):
        for tree in self.tree_sprites.sprites():
            for apple in self.tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()
    
    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.update(dt)
        camera_offset = pygame.math.Vector2(
            SCREEN_WIDTH / 2 - self.Player.rect.centerx,
            SCREEN_HEIGHT / 2 - self.Player.rect.centery
        )
        
        self.all_sprites.customize_draw(self.display_surface, camera_offset)
        
        
        self.overlay.display()
        
        if self.Player.sleep:
            self.transition.play(dt)
        
""" #original code, but the camera didn't work 

        self.display_surface.fill('white')
        #self.all_sprites.draw(self.display_surface)
        self.all_sprites.customize_draw(self.Player)
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
                    
                    
                 