from sound import Sound
from wentity import WEntity
from random import random
from pygame.math import Vector2
from utils import *

WIDTH = 3
SCALE_FACTOR = 3
SPEED = 90.0  # pixels per second
ANGULAR_SPEED = 21.0  # degrees per second
ASTEROID_WIREFRAME = [
    Vector2(-20.0, 20.0), Vector2(-25.0, 5.0), Vector2(-25.0, -10.0),
    Vector2(-5.0, -10.0), Vector2(-10.0, -20.0), Vector2(5.0, -20.0),
    Vector2(20.0, -10.0), Vector2(20.0, -5.0), Vector2(0.0, 0.0),
    Vector2(20.0, 10.0), Vector2(10.0, 20.0), Vector2(0.0, 15.0)
]


class Asteroid(WEntity):

    def __init__(self, galaxy):
        super().__init__(galaxy, "asteroid", WHITE, ASTEROID_WIREFRAME, WIDTH)

        # entity initial position is random
        self.position = Vector2(
            random()*self.galaxy.rect.width, random()*self.galaxy.rect.height)

        # linear velocity in pixels per second at random angle
        self.velocity = Vector2(
            0.0, SPEED * galaxy.get_entity_by_name('score').game_difficulty).rotate(random() * 360.0)

        self.angular_speed = ANGULAR_SPEED
        self.rotating = CLOCKWISE
        self.size = SCALE_FACTOR
        self.times_hit = 0
        self.exploding = False

    def update(self, time_passed, event_list):
        super().update(time_passed, event_list)

        for entity in self.galaxy.get_entities_by_name('blast'):
            if self.collide(entity):
                # if a blast hit me, I need to break myself
                # into 2 smaller rocks !
                self.exploding = True
                self.times_hit += 1
                entity.dead = True # kills the blast
                if self.times_hit < 3:
                    self.size /= 2
                    self.velocity *= 1.5
                    self.velocity.rotate_ip(random()*360)
                    self.galaxy.add_entity(self.fragment())
                else:
                    self.dead = True
                # update score                
                self.galaxy.get_entity_by_name(
                    'score').update_score(+100*self.times_hit)

    def render(self, surface):
        super().render(surface)

        # render sound
        if self.exploding:
            Sound().play('bang')
            self.exploding = False
            
    def fragment(self):
        fragment = Asteroid(self.galaxy)
        fragment.position = Vector2(self.position)
        fragment.velocity = Vector2(self.velocity)
        fragment.velocity.rotate_ip(random()*360)
        fragment.size = self.size
        fragment.times_hit = self.times_hit
        return fragment
