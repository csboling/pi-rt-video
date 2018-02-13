from OpenGL import GL, GLU
import pygame
from pygame.locals import *


from pipeline.playback.pygame import PygameSink


class OpenGLPygameSink(PygameSink):
    def initialize(self, res, flags=0):
        super().initialize(res, flags | DOUBLEBUF | OPENGL)
        
        w, h = res
        # GL.glEnable(GL.GL_DEPTH_TEST)
        # GLU.gluPerspective(45, w / h, 0.1, 50.)
        # GL.glTranslate(0., 0., -5)

    def process(self, item):
        pygame.display.flip()


