from abc import abstractmethod
from io import BytesIO

import numpy as np
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
import pyglet

from pipeline.processor.Processor import Processor
from pipeline.processor.pure import PureFunction


class OpenGLProcessor(Processor):
    def iterate(self):
        t = 0
        for surface in self.source:
            self(surface, t)
            yield surface
            t += 1 / self.framerate

    @abstractmethod
    def __call__(self, surface, t):
        pass


class Clear(OpenGLProcessor):

    def __call__(self, surface, t):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        return surface


class Rotate(OpenGLProcessor):
    def __init__(self, func):
        self.func = func

    def __call__(self, surface, t):
        x, y, z = self.func(t)
        glRotatef(x, 1, 0, 0)
        glRotatef(y, 0, 1, 0)
        glRotatef(z, 0, 0, 1)


class BindTexture(OpenGLProcessor):
    def __init__(self, wireframe, texture, texture_res=(100, 100)):
        self.wireframe = wireframe
        self.texture = texture
        self.texture_res = texture_res

        self.gl_setup()

    def __call__(self, surface, t):
        texture = self.texture(self.texture_res, t)
        quads = self.wireframe.quads(t)
        uv = self.wireframe.uv(t)
        # uv_map = self.wireframe.uv_map(t)
        # vertices = self.wireframe.vertex_map(t)

        self.gl_draw(
            self.to_rgba(texture).astype(np.uint8),
            quads,
            uv,
            # vertices.reshape((-1, 3)),
            # uv_map.reshape((-1, 2))
        )


    def gl_setup(self):
        self.texture_id = glGenTextures(1)
        glTexParameteri(
            GL_TEXTURE_2D, 
            GL_TEXTURE_MAG_FILTER, GL_LINEAR
        )
        glTexParameteri(
            GL_TEXTURE_2D, 
            GL_TEXTURE_MIN_FILTER, GL_LINEAR
        )
    
    def gl_draw(self, texture, quads, uv):
        w, h = texture.shape[:2]

        glEnable(GL_TEXTURE_2D)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(
            GL_TEXTURE_2D, 
            0, GL_RGBA,
            w, h,
            0, GL_RGBA,
            GL_UNSIGNED_BYTE,
            texture
        )
        glGenerateMipmap(GL_TEXTURE_2D)

        for quad_verts, quad_uvs in zip(quads, uv):
            glBegin(GL_QUADS)
            for vertex, uv in zip(quad_verts, quad_uvs):
                glTexCoord2f(*uv)
                glVertex3fv(vertex)
            glEnd()

        glDisable(GL_TEXTURE_2D)

    @staticmethod
    def to_rgba(texture):
        dims, depth = texture.shape[:2], texture.shape[2]
        if depth == 4:
            return texture
        alpha_channel = 255*np.ones((*dims, 1))
        if depth == 3:
            return np.concatenate(
                (texture, alpha_channel), 
                axis=-1
            )
        if depth == 1:
            return np.concatenate(
                (*[texture]*3, alpha_channel),
                axis=-1
            )
        raise TypeError(
            "don't know how to treat shape {} as a texture".format(texture.shape)
        )
