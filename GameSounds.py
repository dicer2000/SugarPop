#############################################################
# Module Name: Sugar Pop Sound Module
# Project: Sugar Pop Program
# Date: Dec 3, 2024
# By: Brett W. Huffman
# Description: The module for playing sounds
#############################################################

from settings import *
import pygame as pg
import pygame.mixer

class GameSounds():
    
    def __init__(self):
        
        # Load the pygame sound engine
        pg.mixer.init()
        self.sounds = {}
        self.load_sounds()
        self.sound_is_mute = False
            
    def load_sounds(self):
        '''Load the sounds from the settings into the sound dictionary'''
        for name, value in SOUNDS.items():
            self.sounds[name] = pygame.mixer.Sound(value)
            
    def play(self, sound_name, loop = False):
        '''Play a sound from the sounds dictionary, indicate if it should loop t/f'''
        # Check if a loop
        loop_val = 0
        if loop:
            loop_val = -1
        # if it exists, play it
        if sound_name in self.sounds:
            # Find an open channel
            for i in range(pygame.mixer.get_num_channels()):
                # At the first open channel, play it
                if pg.mixer.Channel.get_busy(pygame.mixer.Channel(i)) == False:
                    pg.mixer.Channel(i).play(self.sounds[sound_name], loop_val)
                    break
    
    def mute_channel(self, channel):
        '''Mute a particluar channel'''
        pg.mixer.Channel(channel).pause()
        
    def unmute_channel(self, channel):
        '''Unmute a particluar channel'''
        pg.mixer.Channel(channel).unpause()
        
    def mute_all(self):
#        pg.set_volume(0.0)
        pg.mixer.pause()
        self.sound_is_mute = True
        
    def unmute_all(self):
#        pg.set_volume(100.0)
        pg.mixer.unpause()
        self.sound_is_mute = False
        
    def is_mute(self):
        return self.sound_is_mute