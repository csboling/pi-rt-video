from OpenGL import GL, GLU
import pygame
from pygame.locals import *


from pipeline.playback.pygame import PygameSink


class OpenGLPygameSink(PygameSink):
    def initialize(self, res, flags=0):
        super().initialize(res, flags | DOUBLEBUF | OPENGL)
        
        w, h = res
        GLU.gluPerspective(45, w / h, 0.1, 50.)
        GL.glTranslate(0., 0., -5)

    def process(self, item):
        GL.glRotatef(1, 3, 1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.Cube()
        pygame.display.flip()

    @classmethod
    def Cube(cls):
        GL.glBegin(GL.GL_LINES)
        for edge in cls.edges:
            for vertex in edge:
                GL.glVertex3fv(cls.vertices[vertex])
        GL.glEnd()

    vertices = [
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1),
    ]

    edges = [
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7),
    ]
