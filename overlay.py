import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        
        #imports
        overlay_path = "assets/graphics/overlay"
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}/{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}/{seed}.png').convert_alpha() for seed in player.seeds}
        
    def display(self):
        #tool
        tool_surface = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surface.get_rect(midbottom = OVERLAY_POSITIONS["tool"])
        self.display_surface.blit(tool_surface, tool_rect)
        
        #seeds
        seed_surface = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surface.get_rect(midbottom = OVERLAY_POSITIONS["seed"])
        self.display_surface.blit(seed_surface, seed_rect)
        
        
class Transition:
    def __init__(self, reset, player):
    # setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset
        self.player = player
        
        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -3
        
    def play(self):
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -2
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2
        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
 
'''        
class Menu:
    def __init__(self, player, menu):
        self.player = player
        self.menu = menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("assets/font/LycheeSoda.ttf", 30)
        
        #
        self.width = 400
        self.space = 10
        self.padding = 8
        
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border - len(self.player.item_inventory) - 1
        self.setup()
          
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            pass
            #self.menu()
    
    def update(self):
        self.display_surface.blit(pygame.Surface((1000, 1000)), (0,0))

'''