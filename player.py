import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        
        # general setup
        self.image = pygame.Surface((30,60))
        self.image.fill('brown')
        self.rect = self.image.get_rect(center = pos)
    
        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
    
    def move(self, dt):
        # normalize the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
           
    def update(self, dt):
        self.input()
        self.move(dt)