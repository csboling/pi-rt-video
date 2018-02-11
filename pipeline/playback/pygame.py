import numpy as np
import pygame
from pygame.locals import *
from pygame import surfarray

from pipeline.playback.sink import Sink


class PygameSink(Sink):
    def consume(self):
        w, h = self.resolution
        screen = pygame.display.set_mode(
            self.resolution,
            pygame.FULLSCREEN | pygame.NOFRAME
        )

        for item in self.source:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            if isinstance(item, pygame.Surface):
                surface = item
            if isinstance(item, np.ndarray):
                frame = item.swapaxes(0, 1)
                surface = surfarray.make_surface(frame)
            screen.blit(surface, (0, 0))
            pygame.display.flip()
        
