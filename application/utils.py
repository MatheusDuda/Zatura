import pygame

# basic colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BLUESHIELD = (0,206,209)
GREEN = (0,255,0)
CYAN = (0, 255, 255)
RED = 	(255,0,0)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255,140,0)
ORANGERED = (255,69,0)

# game custom events
NEW_GAME = pygame.USEREVENT + 1
START_GAME = pygame.USEREVENT + 2
UNSHIELD_EVENT = pygame.USEREVENT + 3
COUNT_DOWN_EVENT = pygame.USEREVENT + 4
END_RAPID_FIRE_EVENT = pygame.USEREVENT + 5
END_TRIPLE_SHOT_EVENT = pygame.USEREVENT + 6
# game statuses
GAME_NOT_RUNNING = 1
GAME_RUNNING = 2

# entity movements
CLOCKWISE = 1  # rotating clockwise
CCLOCKWISE = -1  # rotating counter clockwise
FORWARD = 1  # accelerating forward