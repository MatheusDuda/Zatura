import os
import pygame
from entity import Entity
from ship import Ship
from pygame import Vector2
from sound import Sound
from utils import *

INITIAL_NUM_LIVES = 3
MAX_LIVES = 5


class Score(Entity):
    def __init__(self, galaxy):
        super().__init__(galaxy, "score", GREEN)
        self.score = 0
        self.font = pygame.font.Font(
            os.path.join('res', 'hyperspace-bold.otf'), 90)
        self.num_lives = INITIAL_NUM_LIVES
        self.ship_shielded = True
        self.game_difficulty = 1.0
        self.game_status = GAME_NOT_RUNNING

    def update(self, time_passed, event_list):
        super().update(time_passed, event_list)
        # build text with current score
        if self.ship_shielded:
            self.text = "{0:,} *".format(self.score)
        else:
            self.text = "{0:,}".format(self.score)
       
        # build number of lives using ship objects
        self.lives = []
        for x in range(50, (self.num_lives*50)+1, 50):
            ship = Ship(self.galaxy)
            ship.position = Vector2(x, 160)
            ship.shielded = False
            self.lives.append(ship)

        # start a new game
        if self.num_lives <= 0 and self.game_status == GAME_RUNNING:
            self.game_status = GAME_NOT_RUNNING
            pygame.time.set_timer(NEW_GAME, 3000, 1)
            Sound().play('siren')
            
    def render(self, surface):
        super().render(surface)
        # render score
        score_surface = self.font.render(self.text, False, self.color)
        surface.blit(score_surface, (30, 5))

        # render number of lives
        for ship in self.lives:
            ship.render(surface)

        # render game over !
        if self.num_lives <= 0:
            game_over_surface = self.font.render(
                'GAME OVER', False, self.color)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.centerx = self.galaxy.rect.centerx
            game_over_rect.centery = self.galaxy.rect.centery - 200
            surface.blit(game_over_surface, game_over_rect)

    def update_score(self, variation):
        self.score += variation

    def update_lives(self, variation):
        self.num_lives += variation
        if self.num_lives < 0:
            self.num_lives = 0
        elif self.num_lives > MAX_LIVES:
            self.num_lives = MAX_LIVES
            
    def update_ship_shielded(self, shielded):
        self.ship_shielded = shielded

    def increase_game_difficulty_by(self, multiplier):
        self.game_difficulty *= multiplier

    def run_game(self):
        self.game_status = GAME_RUNNING
