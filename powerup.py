import pygame
from pygame.math import Vector2
from random import choice, random
from utils import *

# Custom events for power-ups
UNSHIELD_EVENT = pygame.USEREVENT + 1
END_RAPID_FIRE_EVENT = pygame.USEREVENT + 2
END_TRIPLE_SHOT_EVENT = pygame.USEREVENT + 3

# Power-up types configuration
POWERUP_TYPES = {
    'SHIELD': {
        'color': (0, 191, 255),
        'duration': 10,
        'sprite_path': 'res/shield_powerup.png'
    },
    'RAPID_FIRE': {
        'color': (255, 69, 0),
        'duration': 5,
        'sprite_path': 'res/rapid_powerup.png'
    },
    'TRIPLE_SHOT': {
        'color': (50, 205, 50),
        'duration': 7,
        'sprite_path': 'res/triple_powerup.png'
    },
    'EXTRA_LIFE': {
        'color': (255, 20, 147),
        'duration': 0,
        'sprite_path': 'res/life_powerup.png'
    }
}

class PowerUp:
    def __init__(self, galaxy, powerup_type):
        self.galaxy = galaxy
        self.name = "powerup"
        self.dead = False
        self.type = powerup_type
        self.color = POWERUP_TYPES[powerup_type]['color']
        self.duration = POWERUP_TYPES[powerup_type]['duration']
        self.id = None
        self.collected = False
        
        self.wireframe = [
            Vector2(0, -15), Vector2(15, 0),
            Vector2(0, 15), Vector2(-15, 0)
        ]
        
        try:
            self.sprite = pygame.image.load(POWERUP_TYPES[powerup_type]['sprite_path'])
            self.sprite = pygame.transform.scale(self.sprite, (30, 30))
            self.use_sprite = True
        except:
            self.use_sprite = False
        
        margin = 50
        self.position = Vector2(
            margin + random() * (self.galaxy.rect.width - 2 * margin),
            margin + random() * (self.galaxy.rect.height - 2 * margin)
        )
        
        self.velocity = Vector2(30, 0).rotate(random() * 360)
        self.lifetime = 15
        
    def update(self, time_passed, event_list):
        if self.collected:
            return
            
        # Process power-up related events
        for event in event_list:
            if event.type in [UNSHIELD_EVENT, END_RAPID_FIRE_EVENT, END_TRIPLE_SHOT_EVENT]:
                ship = self.galaxy.get_entity_by_name('ship')
                if ship:
                    if event.type == UNSHIELD_EVENT:
                        ship.shielded = False
                    elif event.type == END_RAPID_FIRE_EVENT:
                        ship.rapid_fire = False
                    elif event.type == END_TRIPLE_SHOT_EVENT:
                        ship.triple_shot = False
            
        self.position += self.velocity * time_passed
        
        self.lifetime -= time_passed
        if self.lifetime <= 0:
            self.dead = True
            return
            
        ship = self.galaxy.get_entity_by_name('ship')
        if ship and not self.collected and self.collide(ship):
            self.collected = True
            self.apply_effect(ship)
            self.dead = True
            
    def render(self, surface):
        if self.collected:
            return
            
        if self.use_sprite:
            sprite_rect = self.sprite.get_rect(center=self.position)
            surface.blit(self.sprite, sprite_rect)
        else:
            points = [p + self.position for p in self.wireframe]
            points.append(points[0])
            pygame.draw.lines(surface, self.color, True, points, 2)
            
    def collide(self, other_entity):
        if self.collected:
            return False
            
        collision_distance = 20
        return (self.position - other_entity.position).length() < collision_distance
            
    def apply_effect(self, ship):
        if self.collected:
            return
            
        print(f"Applying power-up effect: {self.type}")
        
        if self.type == 'SHIELD':
            ship.shielded = True
            # Ensure the ship has the shielded attribute
            if not hasattr(ship, 'shielded'):
                setattr(ship, 'shielded', True)
            pygame.time.set_timer(UNSHIELD_EVENT, int(self.duration * 1000), 1)
            
        elif self.type == 'RAPID_FIRE':
            # Ensure the ship has the rapid_fire attribute
            if not hasattr(ship, 'rapid_fire'):
                setattr(ship, 'rapid_fire', True)
            ship.rapid_fire = True
            pygame.time.set_timer(END_RAPID_FIRE_EVENT, int(self.duration * 1000), 1)
            
        elif self.type == 'TRIPLE_SHOT':
            # Ensure the ship has the triple_shot attribute
            if not hasattr(ship, 'triple_shot'):
                setattr(ship, 'triple_shot', True)
            ship.triple_shot = True
            pygame.time.set_timer(END_TRIPLE_SHOT_EVENT, int(self.duration * 1000), 1)
            
        elif self.type == 'EXTRA_LIFE':
            score = self.galaxy.get_entity_by_name('score')
            if score:
                score.update_lives(1)

class PowerUpManager:
    def __init__(self, galaxy):
        self.galaxy = galaxy
        self.spawn_timer = 0
        self.spawn_interval = 15
        self.spawn_chance = 0.7
        self.max_powerups = 3
        print("PowerUpManager initialized")
        
    def update(self, time_passed):
        self.spawn_timer += time_passed
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            if random() < self.spawn_chance:
                self.spawn_power_up()
            
    def spawn_power_up(self):
        existing_powerups = [e for e in self.galaxy.entities.values() 
                           if e.name == "powerup" and not e.collected]
        
        if len(existing_powerups) < self.max_powerups:
            powerup_type = choice(list(POWERUP_TYPES.keys()))
            new_powerup = PowerUp(self.galaxy, powerup_type)
            self.galaxy.add_entity(new_powerup)
            print(f"Spawned {powerup_type} power-up at {new_powerup.position}")