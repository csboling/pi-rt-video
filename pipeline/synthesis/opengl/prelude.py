from glumpy import gl, glm
import numpy as np

from pipeline.processor.Processor import TimeProcessor
from pipeline.utils import params, Parameter


class OpenGLProcessor(TimeProcessor):
    pass


class Clear(OpenGLProcessor):

    @params(color=[0, 0, 0, 1])
    def __init__(self, color):
        self.color = color
    
    def __call__(self, surface, t):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glClearColor(*self.color(t))
        return surface

    
class Rotation(Parameter):
    
    @params(angle=None, matrix=lambda t: np.eye(4))
    def __init__(self, angle, matrix):
        self.angle = angle
        self.matrix = matrix

    def __call__(self, t):
        alpha, beta, gamma = self.angle(t)
        matrix = self.matrix(t)
        glm.rotate(matrix, alpha, 1, 0, 0)
        glm.rotate(matrix, beta,  0, 1, 0)
        glm.rotate(matrix, gamma, 0, 0, 1)
        return matrix


class Translation(Parameter):
    @params(r=None, matrix=lambda t: np.eye(4))
    def __init__(self, r, matrix):
        self.r = r
        self.matrix = matrix

    def __call__(self, t):
        r = self.r(t)
        matrix = self.matrix(t)
        glm.translate(matrix, *r)
        return matrix
