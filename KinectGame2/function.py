import sys, pygame

from pygame.locals import *

import pygame.mixer

def playsong(filename):
    pygame.init()
    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(filename)
        sound.play()
    except pygame.error, message:
      print 'Cannot play song : ', filename