import pygame
from pygame.locals import *
from asteroid import Asteroid
from countdown import CountDown
from galaxy import Galaxy
from score import Score
from ship import Ship
from fps import Fps
from utils import *
from menu import MainMenu
from powerup import UNSHIELD_EVENT, END_RAPID_FIRE_EVENT, END_TRIPLE_SHOT_EVENT

COLOR_DEPTH = 8
FPS = 50
NUMBER_ASTEROIDS = 7

class Game():
    def __init__(self):
        pygame.init()


        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN, depth=COLOR_DEPTH)
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Asteroids arcade game")
        self.clock = pygame.time.Clock()
        self.game_state = "MENU"
        self.galaxy = None
        self.fps = None
        self.score = None
        self.powerup_events = [UNSHIELD_EVENT, END_RAPID_FIRE_EVENT, END_TRIPLE_SHOT_EVENT]
        
        # Create main menu
        self.main_menu = MainMenu(self.screen, self)

    def new_game(self):
        # Limpar todos os timers de power-ups ativos
        for event in self.powerup_events:
            pygame.time.set_timer(event, 0)  # Desativa o timer
            
        # Initialize game components
        self.galaxy = Galaxy(self.screen_rect)
        self.galaxy.add_entity(Ship(self.galaxy))
        self.fps = Fps(self.galaxy)
        self.galaxy.add_entity(self.fps)
        self.score = Score(self.galaxy)
        self.galaxy.add_entity(self.score)
        for i in range(NUMBER_ASTEROIDS):
            self.galaxy.add_entity(Asteroid(self.galaxy))
        self.galaxy.add_entity(CountDown(self.galaxy))

    def handle_powerup_event(self, event):
        if not self.galaxy:
            return
            
        ship = self.galaxy.get_entity_by_name('ship')
        if not ship:
            return
            
        if event.type == UNSHIELD_EVENT:
            ship.shielded = False
        elif event.type == END_RAPID_FIRE_EVENT:
            ship.rapid_fire = False
        elif event.type == END_TRIPLE_SHOT_EVENT:
            ship.triple_shot = False

    def run(self):
        done = False
        while not done:
            if self.game_state == "MENU":
                menu_result = self.main_menu.run()
                if menu_result == "QUIT":
                    done = True
                
            elif self.game_state == "PLAYING":
                event_list = pygame.event.get()
                
                for event in event_list:
                    if event.type == KEYDOWN:
                        if event.key == K_q:
                            done = True
                        elif event.key == K_ESCAPE:
                            # Limpar timers ao voltar para o menu
                            for event_type in self.powerup_events:
                                pygame.time.set_timer(event_type, 0)
                            self.game_state = "MENU"
                            self.main_menu.active = True
                            continue
                    elif event.type == QUIT:
                        done = True
                    elif event.type == NEW_GAME:
                        self.new_game()
                    elif event.type in self.powerup_events:
                        self.handle_powerup_event(event)

                if self.galaxy:
                    asteroids = self.galaxy.get_entities_by_name('asteroid')
                    if len(asteroids) == 0:
                        # Impedir múltiplos NEW_GAME events
                        existing_countdowns = self.galaxy.get_entities_by_name('countdown')
                        if not existing_countdowns:
                            self.score.increase_game_difficulty_by(1.11)
                            self.score.update_lives(+1)
                            for i in range(NUMBER_ASTEROIDS):
                                self.galaxy.add_entity(Asteroid(self.galaxy))

                    time_passed = self.clock.tick(FPS)
                    if self.fps:
                        self.fps.update_fps(self.clock.get_fps())
                    
                    self.galaxy.update(time_passed, event_list)
                    self.galaxy.render(self.screen)
                    self.galaxy.cleanup()
                    
                    # Verificar se o jogador morreu
                    ship = self.galaxy.get_entity_by_name('ship')
                    if not ship:
                        pygame.event.post(pygame.event.Event(NEW_GAME))
                    
                    pygame.display.flip()

        # Limpar todos os timers ao sair do jogo
        for event_type in self.powerup_events:
            pygame.time.set_timer(event_type, 0)
        pygame.quit()

if __name__ == "__main__":
    Game().run()