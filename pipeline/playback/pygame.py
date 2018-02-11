import numpy as np
import pygame
from pygame.locals import *
from pygame import surfarray

from pipeline.playback.sink import Sink


class PygameSink(Sink):
    def consume(self):
        self.initialize(self.resolution)
        for item in self.source:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.process(item)
            
    def process(self, item):
        if isinstance(item, pygame.Surface):
            surface = item
        if isinstance(item, np.ndarray):
            frame = item.swapaxes(0, 1)
            surface = surfarray.make_surface(frame)
        screen.blit(surface, (0, 0))
        pygame.display.flip()
    

    def initialize(self, res, flags=0):
        pygame.init()
        screen = pygame.display.set_mode(res, flags | pygame.FULLSCREEN)

