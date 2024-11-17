import os
import pygame
from pygame import mixer

class Sound:
    _instance = None
    _sounds = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sound, cls).__new__(cls)
            
            # Volume inicial para cada tipo de som
            cls._volume_settings = {
                'sfx': 0.2,    # Efeitos sonoros
                'music': 0.2,  # Música de fundo
                'master': 1.0  # Volume master
            }
            
            # Configurar mixer
            mixer.init()
            
            # Carregar sons com categorias
            cls._sounds = {
                'bang': {
                    'sound_key': mixer.Sound(os.path.join('res', 'bang.wav')),
                    'channel': mixer.Channel(0),
                    'overlap': True,
                    'category': 'sfx'
                },
                'beep': {
                    'sound_key': mixer.Sound(os.path.join('res', 'beep.wav')),
                    'channel': mixer.Channel(2),
                    'overlap': True,
                    'category': 'sfx'
                },
                'fire': {
                    'sound_key': mixer.Sound(os.path.join('res', 'fire.wav')),
                    'channel': mixer.Channel(2),
                    'overlap': True,
                    'category': 'sfx'
                },
                'siren': {
                    'sound_key': mixer.Sound(os.path.join('res', 'siren.wav')),
                    'channel': mixer.Channel(2),
                    'overlap': True,
                    'category': 'sfx'
                },
                'thrust': {
                    'sound_key': mixer.Sound(os.path.join('res', 'thrust.wav')),
                    'channel': mixer.Channel(1),
                    'overlap': False,
                    'category': 'sfx'
                },
                'beep-countdown': {
                    'sound_key': mixer.Sound(os.path.join('res', 'beep-countdown.wav')),
                    'channel': mixer.Channel(2),
                    'overlap': True,
                    'category': 'sfx'
                },
                'powerup': {
                    'sound_key': mixer.Sound(os.path.join('res', 'powerup.wav')),
                    'channel': mixer.Channel(3),
                    'overlap': True,
                    'category': 'sfx'
                }
            }
            
            # Aplicar volumes iniciais
            cls._instance._update_all_volumes()
            
        return cls._instance
    
    def play(self, sound_key):
        sound = self._sounds[sound_key]
        if sound['overlap'] or not sound['overlap'] and not sound['channel'].get_busy():
            sound['channel'].play(sound['sound_key'])
    
    def set_volume(self, category, value):
        """Define o volume para uma categoria (0.0 a 1.0)"""
        self._volume_settings[category] = max(0.0, min(1.0, value))
        self._update_all_volumes()
    
    def get_volume(self, category):
        """Retorna o volume atual de uma categoria"""
        return self._volume_settings[category]
    
    def _update_all_volumes(self):
        """Atualiza o volume de todos os sons baseado nas configurações"""
        master = self._volume_settings['master']
        for sound_info in self._sounds.values():
            category_vol = self._volume_settings[sound_info['category']]
            final_volume = master * category_vol
            sound_info['sound_key'].set_volume(final_volume)