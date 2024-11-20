import pygame
import os
from pygame.math import Vector2
from utils import *
from sound import Sound

class MenuItem:
    def __init__(self, text, position, callback, font_size=70):
        self.text = text
        self.position = position
        self.callback = callback
        self.font = pygame.font.Font(os.path.join('res', 'Prida.otf'), font_size)
        self.selected = False
        
    def render(self, surface):
        color = ORANGE if self.selected else WHITE
        text_surface = self.font.render(self.text, True, color)
        rect = text_surface.get_rect(center=self.position)
        surface.blit(text_surface, rect)
        
    def handle_click(self, pos):
        rect = self.font.render(self.text, True, WHITE).get_rect(center=self.position)
        if rect.collidepoint(pos):
            self.callback()
            return True
        return False

class MainMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.active = True

        sound = Sound()
        sound.play('background_music')
        
        try:
            self.logo = pygame.image.load(os.path.join('res', 'logo.png'))
        except:
            self.logo = None
            
        screen_center = Vector2(self.screen.get_rect().center)
        self.menu_items = [
            MenuItem("JOGAR", screen_center + Vector2(0, 50), lambda: self.start_game()),
            MenuItem("TUTORIAL", screen_center + Vector2(0, 120), self.show_tutorial),
            MenuItem("OPÇÕES", screen_center + Vector2(0, 190), self.show_options),
            MenuItem("SAIR", screen_center + Vector2(0, 260), self.quit_game)
        ]
        
        self.selected_item = 0
        self.menu_items[self.selected_item].selected = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_items[self.selected_item].selected = False
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    self.menu_items[self.selected_item].selected = True
                    Sound().play('beep')
                    
                elif event.key == pygame.K_DOWN:
                    self.menu_items[self.selected_item].selected = False
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    self.menu_items[self.selected_item].selected = True
                    Sound().play('beep')
                    
                elif event.key == pygame.K_RETURN:
                    self.menu_items[self.selected_item].callback()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    for item in self.menu_items:
                        if item.handle_click(event.pos):
                            break
                            
        return True
        
    def render(self):
        self.screen.fill(BLACK)
        
        if self.logo:
            logo_rect = self.logo.get_rect(center=(self.screen.get_rect().centerx, 100))
            self.screen.blit(self.logo, logo_rect)
        else:
            font = pygame.font.Font(os.path.join('res', 'Prida.otf'), 150)
            title = font.render("Zatura", True, ORANGE)
            title_rect = title.get_rect(center=(self.screen.get_rect().centerx, 300))
            self.screen.blit(title, title_rect)
        
        for item in self.menu_items:
            item.render(self.screen)
            
        pygame.display.flip()
        
    def start_game(self):
        self.active = False
        self.game.game_state = "PLAYING"
        pygame.event.post(pygame.event.Event(NEW_GAME))

    def show_tutorial(self):
        tutorial = TutorialMenu(self.screen, self.game)
        tutorial.run()

    def show_options(self):
        options = OptionsMenu(self.screen, self.game)
        options.run()
        
    def quit_game(self):
        pygame.quit()
        exit()
        
    def run(self):
        while self.active:
            if not self.handle_input():
                self.quit_game()
            self.render()
            pygame.time.Clock().tick(60)

class TutorialMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.active = True
        
        # Configurações de fonte
        self.title_font = pygame.font.Font(os.path.join('res', 'Prida.otf'), 100)
        self.text_font = pygame.font.Font(os.path.join('res', 'Prida.otf'), 40)
        
        # Texto explicativo dos controles no estilo instructions
        self.tutorial_text = [
            ("Movimentação:", ORANGE, "", WHITE),
            ("← → ou A D :", ORANGE, "Girar a nave", WHITE),
            ("↑ ou W :", ORANGE, "Acelerar", WHITE),
            ("ESPAÇO :", ORANGE, "Atirar", WHITE),
            ("", BLACK, "", BLACK),
            ("", BLACK, "", BLACK),
            ("POWER-UPS:", ORANGE, "", WHITE),
            ("Azul :", ORANGE, "Protege contra colisões", WHITE),
            ("Verde :", ORANGE, "Atira 3 projéteis", WHITE),
            ("Vermelho ", ORANGE, "Aumenta velocidade de tiro", WHITE),
            ("Rosa : ", ORANGE, "Adiciona uma vida", WHITE)
        ]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    return True
        return True
        
    def render(self):
        self.screen.fill(BLACK)
        
        # Renderiza título
        title = self.title_font.render("TUTORIAL", True, ORANGE)
        title_rect = title.get_rect(center=(self.screen.get_rect().centerx, 100))
        self.screen.blit(title, title_rect)
        
        # Renderiza texto de controles
        y_pos = 250
        for highlight, highlight_color, description, description_color in self.tutorial_text:
            # Renderiza parte destacada
            highlight_surf = self.text_font.render(highlight, True, highlight_color)
            highlight_width = highlight_surf.get_width()

            # Renderiza parte descritiva
            description_surf = self.text_font.render(description, True, description_color)
            description_width = description_surf.get_width()

            # Calcula largura total para centralizar
            total_width = highlight_width + description_width
            start_x = (self.screen.get_width() - total_width) // 2
            
            # Renderiza texto destacado
            self.screen.blit(highlight_surf, (start_x, y_pos))
            # Renderiza texto descritivo após o texto destacado
            self.screen.blit(description_surf, (start_x + highlight_width, y_pos))

            y_pos += 50  # Espaço entre cada instrução
        
        # Renderiza instruções para voltar
        back_text = self.text_font.render("ESC ",True, ORANGE)
        back_desc = self.text_font.render(": Voltar",True, WHITE)
        back_width = back_text.get_width() + back_desc.get_width()
        start_x = (self.screen.get_width() - back_width) // 2
        
        self.screen.blit(back_text, (start_x, 900))
        self.screen.blit(back_desc, (start_x + back_text.get_width(), 900))
        
        pygame.display.flip()
        
    def run(self):
        while self.active:
            if not self.handle_input():
                pygame.quit()
                exit()
            self.render()
            pygame.time.Clock().tick(60)

class OptionsMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.active = True
        self.sound = Sound()
        
        # Configurar controles de volume
        center_x = self.screen.get_rect().centerx
        self.volume_controls = [
            {
                'name': 'Volume Principal',
                'category': 'master',
                'position': Vector2(center_x, 200)
            },
            {
                'name': 'Volume SFX',
                'category': 'sfx',
                'position': Vector2(center_x, 280)
            },
            {
                'name': 'Volume Música',
                'category': 'music',
                'position': Vector2(center_x, 360)
            }
        ]
        
        self.selected_control = 0
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active = False
                    
                elif event.key == pygame.K_UP:
                    self.selected_control = (self.selected_control - 1) % len(self.volume_controls)
                    Sound().play('beep')
                    
                elif event.key == pygame.K_DOWN:
                    self.selected_control = (self.selected_control + 1) % len(self.volume_controls)
                    Sound().play('beep')
                    
                elif event.key == pygame.K_LEFT:
                    current = self.volume_controls[self.selected_control]
                    current_vol = self.sound.get_volume(current['category'])
                    new_vol = max(0.0, current_vol - 0.1)
                    self.sound.set_volume(current['category'], new_vol)
                    Sound().play('beep')
                    
                elif event.key == pygame.K_RIGHT:
                    current = self.volume_controls[self.selected_control]
                    current_vol = self.sound.get_volume(current['category'])
                    new_vol = min(1.0, current_vol + 0.1)
                    self.sound.set_volume(current['category'], new_vol)
                    Sound().play('background_music')
                    
        return True
        
    def render(self):
        self.screen.fill(BLACK)
        
        # Render title
        font = pygame.font.Font(os.path.join('res', 'Prida.otf'), 100)
        title = font.render("OPÇÕES", True, ORANGE)
        title_rect = title.get_rect(center=(self.screen.get_rect().centerx, 150))
        self.screen.blit(title, title_rect)
        
        # Render volume controls
        control_font = pygame.font.Font(os.path.join('res', 'Prida.otf'), 55)
        
        for i, control in enumerate(self.volume_controls):
            # Render control name
            color = ORANGE if i == self.selected_control else WHITE
            text = control_font.render(control['name'], True, color)
            text_rect = text.get_rect(center=(control['position'].x - 200, control['position'].y + 180))
            self.screen.blit(text, text_rect)
            
            # Render volume bar
            bar_width = 200
            bar_height = 20
            bar_x = control['position'].x + 200
            bar_y = control['position'].y +180 - bar_height / 2
            
            # Background bar
            pygame.draw.rect(self.screen, ORANGE, 
                            (bar_x, bar_y, bar_width, bar_height), 2)
            
            # Fill bar based on volume
            volume = self.sound.get_volume(control['category'])
            fill_width = int(bar_width * volume)
            if fill_width > 0:
                pygame.draw.rect(self.screen, WHITE,
                                (bar_x+2, bar_y+2, fill_width-4, bar_height-4))
        
        # Render instructions
        inst_font = pygame.font.Font(os.path.join('res', 'Prida.otf'), 40)
        instructions = [
            ("↑↓ ", ORANGE, "Selecionar Opção", WHITE),
            ("←→ ", ORANGE, "Ajustar Volume", WHITE),
            ("ESC ", ORANGE, ": Voltar", WHITE)
        ]
        
        y_pos = 750
        for highlight, highlight_color, description, description_color in instructions:
            # Render highlighted part (e.g., arrows or ESC)
            highlight_surf = inst_font.render(highlight, True, highlight_color)
            highlight_width = highlight_surf.get_width()

            # Render description part
            description_surf = inst_font.render(description, True, description_color)
            description_width = description_surf.get_width()

            # Calculate total width for centering
            total_width = highlight_width + description_width
            start_x = (self.screen.get_width() - total_width) // 2
            
            # Render highlight text
            self.screen.blit(highlight_surf, (start_x, y_pos))
            # Render description text after the highlighted text
            self.screen.blit(description_surf, (start_x + highlight_width, y_pos))

            y_pos += 40  # Space between each instruction
        
        pygame.display.flip()

    def run(self):
        while self.active:
            if not self.handle_input():
                pygame.quit()
                exit()
            self.render()
            pygame.time.Clock().tick(60)