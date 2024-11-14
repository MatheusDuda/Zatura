import os
import pygame


class Sound():
    """Load game sounds and make them available to play.
    This class follows the singleton design pattern. """
    _instance = None
    _sounds = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sound, cls).__new__(cls)
            cls._sounds = {
                'bang': {
                    'sound_key': pygame.mixer.Sound(os.path.join('res', 'bang.wav')),
                    'channel': pygame.mixer.Channel(0),
                    'overlap': True
                },
                'beep': {
                    'sound_key': pygame.mixer.Sound(os.path.join('res', 'beep.wav')),
                    'channel': pygame.mixer.Channel(2),
                    'overlap': True
                },
                'fire': {
                    'sound_key': pygame.mixer.Sound(os.path.join('res', 'fire.wav')),
                    'channel': pygame.mixer.Channel(2),
                    'overlap': True
                },
                'siren': {
                    'sound_key': pygame.mixer.Sound(os.path.join('res', 'siren.wav')),
                    'channel': pygame.mixer.Channel(2),
                    'overlap': True
                },
                'thrust': {
                    'sound_key': pygame.mixer.Sound(os.path.join('res', 'thrust.wav')),
                    'channel': pygame.mixer.Channel(1),
                    'overlap': False
                },
                'beep-countdown': {
                    'sound_key': pygame.mixer.Sound(os.path.join('res', 'beep-countdown.wav')),
                    'channel': pygame.mixer.Channel(2),
                    'overlap': True
                }
            }
        return cls._instance

    def play(self, sound_key):
        sound = self._sounds[sound_key]['sound_key']
        channel = self._sounds[sound_key]['channel']
        overlap = self._sounds[sound_key]['overlap']
        if overlap or not overlap and not channel.get_busy():
            channel.play(sound)
        