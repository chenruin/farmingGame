import pygame
from settings import *
from settings import LAYERS
from random import *
from timer import Timer

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
        apple_images = {
        "red": "assets/graphics/fruit/Apple Red.png",
        "green": "assets/graphics/fruit/Apple Green.png",
        "yellow": "assets/graphics/fruit/Apple Yellow.png",
        }
        self.apple_surf = pygame.image.load(apple_images["red"])
        self.apple_pos = FRUITS_POS["RED APPLE"]
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
                Generic(
                    pos = (x, y), 
                    surf=self.apple_surf, 
                    groups=[self.apple_sprites, self.groups()[0]],
                    z = LAYERS["fruit"])