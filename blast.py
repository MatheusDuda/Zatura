from wentity import WEntity
from pygame.math import Vector2
from utils import *

WIDTH = 3  # line thickness
SCALE_FACTOR = 3
SPEED = 700.0  # pixels per second
BLAST_WIREFRAME = [
    Vector2(0.5, 0.0),  Vector2(-0.5, -1.0),
    Vector2(0.5, -2.0), Vector2(-0.5, -3.0)
]


class Blast(WEntity):
    def __init__(self, galaxy, position, angle):
        super().__init__(galaxy, "blast", GREEN, BLAST_WIREFRAME, WIDTH)
        
        self.position = position
        self.velocity = Vector2(0.0, -SPEED).rotate(angle)
        self.size = SCALE_FACTOR
