from pygame.locals import *
from blast import Blast
from sound import Sound 
from wentity import WEntity
from pygame.math import Vector2
from utils import *
from powerup import END_RAPID_FIRE_EVENT, END_TRIPLE_SHOT_EVENT
import math

WIDTH = 3  # line thickness
SCALE_FACTOR = 5.0
ACCELERATION = 250.0  # pixels per second
DAMPING = 0.57  # some damping
ANGULAR_SPEED = 180.0  # degrees per second
SHIP_WIREFRAME = [
    Vector2(0.0, -5.0),  Vector2(3.0, 4.0), Vector2(1.5, 2.0),
    Vector2(-1.5, 2.0), Vector2(-3.0, 4.0)
]
THRUST_WIREFRAME = [
    Vector2(1.0, 2.0), Vector2(0.0, 5.0), Vector2(-1.0, 2.0)
]

# Configurações de tiro
NORMAL_FIRE_DELAY = 0.25  # segundos entre tiros normais
RAPID_FIRE_DELAY = 0.1   # segundos entre tiros rápidos
TRIPLE_SHOT_SPREAD = 15  # ângulo entre tiros do triple shot

class Ship(WEntity):
    def __init__(self, galaxy):
        super().__init__(galaxy, "ship", GREEN, SHIP_WIREFRAME, WIDTH)

        # ship initial position
        self.position = Vector2(self.galaxy.rect.width/2,
                              self.galaxy.rect.height/2)
        self.acceleration = ACCELERATION
        self.damping = DAMPING 
        self.angular_speed = ANGULAR_SPEED
        self.size = SCALE_FACTOR
        self.shielded = True
        self.firing = False 
        self.dying = False
        
        # Power-up states
        self.rapid_fire = False
        self.triple_shot = False
        self.fire_timer = 0
        self.can_fire = True
        
    def update(self, time_passed, event_list):
        super().update(time_passed, event_list)

        if self.galaxy.get_entity_by_name('score').game_status != GAME_RUNNING:
            return

        self.process_events(event_list)
        
        # Atualiza timer de tiro
        if not self.can_fire:
            self.fire_timer += time_passed
            fire_delay = RAPID_FIRE_DELAY if self.rapid_fire else NORMAL_FIRE_DELAY
            if self.fire_timer >= fire_delay:
                self.can_fire = True
                self.fire_timer = 0
        
        if self.firing and self.can_fire:
            self.shoot()
            self.can_fire = False
            self.fire_timer = 0

        for entity in self.galaxy.get_entities_by_name('asteroid'):
            if not self.shielded and self.collide(entity):
                self.dying = True
                self.shield()
                pygame.time.set_timer(UNSHIELD_EVENT, 2500, 1)
                self.position = Vector2(self.galaxy.rect.width/2,
                                      self.galaxy.rect.height/2)
                self.velocity = Vector2(0.0, 0.0)
                self.angle = 0.0
                self.galaxy.get_entity_by_name('score').update_lives(-1)

    def shoot(self):
        if self.triple_shot:
            # Tiro central
            self.create_blast(self.angle)
            # Tiros laterais
            self.create_blast(self.angle - TRIPLE_SHOT_SPREAD)
            self.create_blast(self.angle + TRIPLE_SHOT_SPREAD)
        else:
            self.create_blast(self.angle)
            
    def create_blast(self, angle):
        blast = Blast(self.galaxy, Vector2(self.position), angle)
        self.galaxy.add_entity(blast)

    def render(self, surface):
        super().render(surface)

        if self.accelerating == FORWARD:
            Sound().play('thrust')
            self.wireframe = THRUST_WIREFRAME
            super().render(surface)
            self.wireframe = SHIP_WIREFRAME

        if self.firing and self.can_fire:
            Sound().play('fire')
            
        if self.dying:
            Sound().play('bang')
            self.dying = False

    def process_events(self, event_list):
        for event in event_list:
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    self.start_rotating(CCLOCKWISE)
                if event.key == K_RIGHT or event.key == K_d:
                    self.start_rotating(CLOCKWISE)
                if event.key == K_UP or event.key == K_w:
                    self.start_accelerating(FORWARD)
                if event.key == K_SPACE:
                    self.fire()

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a or \
                   event.key == K_RIGHT or event.key == K_d:
                    self.stop_rotating()
                if event.key == K_UP or event.key == K_w:
                    self.stop_accelerating()
                if event.key == K_SPACE:
                    self.firing = False

            if event.type == UNSHIELD_EVENT:
                self.unshield()
            elif event.type == END_RAPID_FIRE_EVENT:
                self.rapid_fire = False
            elif event.type == END_TRIPLE_SHOT_EVENT:
                self.triple_shot = False

    def fire(self): 
        self.firing = True

    def unshield(self):
        self.shielded = False
        self.galaxy.get_entity_by_name('score').update_ship_shielded(False)

    def shield(self):
        self.shielded = True
        self.galaxy.get_entity_by_name('score').update_ship_shielded(True)