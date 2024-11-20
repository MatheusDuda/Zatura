import os
import pygame
from entity import Entity
from utils import *


class Fps(Entity):
    def __init__(self, galaxy):
        super().__init__(galaxy, "fps", GREEN)
        self.fps = 0.0
        self.font = pygame.font.Font(os.path.join(
            'res', 'hyperspace-bold.otf'), 20)

    def update(self, time_passed, event_list):
        super().update(time_passed, event_list)
        self.text = "FPS = {0:.1f}".format(self.fps)

    def render(self, surface):
        super().render(surface)        
        fps_surface = self.font.render(self.text, False, self.color)
        rect = fps_surface.get_rect()
        rect.right = self.galaxy.rect.right - 21
        rect.y = 21
        surface.blit(fps_surface, rect)

    def update_fps(self, fps):
        self.fps = fps
