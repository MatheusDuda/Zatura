from pygame import Vector2


class Entity():

    def __init__(self, galaxy, name, color):
        self.galaxy = galaxy
        self.name = name
        self.color = color
        self.position = Vector2(0.0, 0.0)
        self.dead = False 

    def update(self, time_passed, event_list):
        pass

    def render(self, surface):
        pass
