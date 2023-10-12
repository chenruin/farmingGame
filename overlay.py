import pygame
from settings import *

class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        
        #imports
        #/Users/chenrui/Documents/classes/2023 fall/hci 584/farming simulator/s1 - setup/graphics/overlay/axe.png
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
        