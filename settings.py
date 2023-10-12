from pygame.math import Vector2

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
    "tool" : (SCREEN_WIDTH / 2 - 30, SCREEN_HEIGHT - 15),
    "seed" : (SCREEN_WIDTH / 2 + 30, SCREEN_HEIGHT - 15)
}

# layers of each element of sprite
LAYERS = {
    "water" : 0,
    "ground" : 1,
    "soil" : 2,
    "soil water" : 3,
    "rain floor" : 4,
    "house floor" : 5,
    "ground plant" : 6,
    "main" : 7,
    "house top" : 8,
    "fruit": 9,
    "rain drops" : 10
    
}