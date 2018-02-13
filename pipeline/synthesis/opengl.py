from abc import abstractmethod
from io import BytesIO

from glumpy import gl, glm, gloo

import numpy as np
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
import pyglet

from pipeline.processor.Processor import Processor
from pipeline.processor.pure import PureFunction
from pipeline.synthesis import geometry
from pipeline.utils import params, Parameter


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


class Shader(OpenGLProcessor):
    def __init__(self, program, line_mode=gl.GL_TRIANGLE_STRIP):
        self.program = program
        self.line_mode = line_mode
    
    def __call__(self, surface, t):
        self.draw()
        return self

    def draw(self):
        self.program.draw(self.line_mode)
        

class ColorSquare(Shader):
    @params(corner_colors=None)
    def __init__(self, corner_colors):
        super().__init__(
            gloo.Program(
                vertex="""
                uniform float scale;
                attribute vec2 position;
                attribute vec4 color;
                varying vec4 v_color;

                void main()
                {
                    gl_Position = vec4(scale*position, 0.0, 1.0);
                    v_color = color;
                } 
                """,
                fragment="""
                varying vec4 v_color;

                void main()
                {
                    gl_FragColor = v_color;
                } 
                """,
                count=4
            ),
        )

        self.corner_colors = corner_colors
        self.position = [
            [-1,-1],
            [-1,+1],
            [+1,-1],
            [+1,+1],
        ]

    def __call__(self, surface, t):
        self.program['color'] = self.corner_colors(t)
        self.program['position'] = self.position
        self.program['scale'] = 1.0
        return super().__call__(surface, t)
        
        
class Perspective(Shader):
    @params(
        positions=None,
        indices=None,
        model=np.eye(4, dtype=np.float32),
        view=geometry.translation_matrix((0, 0, -5)),
        projection=np.eye(4, dtype=np.float32),
    )
    def __init__(self,
                 vertex_count, positions, indices,
                 model, view, projection,
                 *args, **kwargs):
        self.positions = positions
        self.indices = indices
        self.model = model
        self.view = view
        self.projection = projection

        gl.glEnable(gl.GL_DEPTH_TEST)
        
        super().__init__(gloo.Program(
            vertex='''
            uniform mat4 u_model;
            uniform mat4 u_view;
            uniform mat4 u_projection;

            attribute vec3 a_position;

            void main()
            {
                gl_Position = u_projection *
                              u_view *
                              u_model *
                              vec4(a_position, 1.0);
            }
            ''',
            fragment='''
            void main()
            {
                gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
            '''
        ), *args, **kwargs)

        self.vertex_buffer = np.zeros(
            vertex_count,
            [('a_position', np.float32, 3)]
        ).view(gloo.VertexBuffer)

    def __call__(self, surface, t):
        self.vertex_buffer['a_position'] = self.positions(t)
        self.index_buffer = self.indices(t).view(gloo.IndexBuffer)
        self.program.bind(self.vertex_buffer)
        
        self.program['u_model'] = self.model(t)
        self.program['u_view'] = self.view(t)
        self.program['u_projection'] = self.projection(t)

        return super().__call__(surface, t)
        
    def draw(self):
        self.program.draw(self.line_mode, self.index_buffer)


class WireframePerspective(Perspective):
    def __init__(self, wireframe, *args, **kwargs):
        positions = wireframe.verts.reshape((-1, 3))
        super().__init__(
            vertex_count=positions.shape[0],
            positions=positions,
            indices=wireframe.inds.reshape((-1,)),
            *args, **kwargs
        )


class Rotation(Parameter):
    @params(angle=None, matrix=None)
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
        
    
# class TexturedSphere(OpenGLProcessor):

#     def __init__(self, texture, texture_res=(112, 112)):
#         self.texture = texture
#         self.texture_res = texture_res

#         self.texture_id = glGenTextures(1)
#         self.sphere = gluNewQuadric()


#     def __del__(self):
#         gluDeleteQuadric(self.sphere)

#     def __call__(self, surface, t):
#         texture = self.texture(self.texture_res, t)
#         w, h = texture.shape[:2]

#         glEnable(GL_TEXTURE_2D)
#         glBindTexture(GL_TEXTURE_2D, self.texture_id)
#         glTexParameteri(
#             GL_TEXTURE_2D,
#             GL_TEXTURE_MAG_FILTER, GL_LINEAR
#         )
#         glTexParameteri(
#             GL_TEXTURE_2D,
#             GL_TEXTURE_MIN_FILTER, GL_LINEAR
#         )
#         glTexImage2D(
#             GL_TEXTURE_2D,
#             0, GL_RGB,
#             w, h,
#             0, GL_RGB,
#             GL_UNSIGNED_BYTE,
#             np.flip(texture, axis=-1).astype(np.uint8)
#         )
#         glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
#         gluQuadricTexture(self.sphere, GL_TRUE)
#         gluQuadricDrawStyle(self.sphere, GLU_FILL)
#         gluQuadricNormals(self.sphere, GLU_SMOOTH)
#         gluSphere(self.sphere, 1.5, 20, 20)

#         glDisable(GL_TEXTURE_2D)

#     @staticmethod
#     def to_rgba(texture):
#         dims, depth = texture.shape[:2], texture.shape[2]
#         if depth == 4:
#             return texture
#         alpha_channel = 255*np.ones((*dims, 1))
#         if depth == 3:
#             return np.concatenate(
#                 (texture, alpha_channel),
#                 axis=-1
#             )
#         if depth == 1:
#             return np.concatenate(
#                 (*[texture]*3, alpha_channel),
#                 axis=-1
#             )
#         raise TypeError(
#             "don't know how to treat shape {} as a texture".format(texture.shape)
#         )




# class Rotate(OpenGLProcessor):
#     def __init__(self, func):
#         self.func = func

#     def __call__(self, surface, t):
#         x, y, z = self.func(t)
#         glRotatef(x, 1, 0, 0)
#         glRotatef(y, 0, 1, 0)
#         glRotatef(z, 0, 0, 1)


# class BindTexture(OpenGLProcessor):
#     def __init__(self, wireframe, texture, texture_res=(100, 100)):
#         self.wireframe = wireframe
#         self.texture = texture
#         self.texture_res = texture_res

#         self.gl_setup()

#     def __call__(self, surface, t):
#         texture = self.texture(self.texture_res, t)
#         quads = self.wireframe.quads(t)
#         uv = self.wireframe.uv(t)

#         self.gl_draw(
#             self.to_rgba(texture).astype(np.uint8),
#             quads,
#             uv,
#         )

#     def gl_setup(self):
#         self.texture_id = glGenTextures(1)
#         glTexParameteri(
#             GL_TEXTURE_2D, 
#             GL_TEXTURE_MAG_FILTER, GL_LINEAR
#         )
#         glTexParameteri(
#             GL_TEXTURE_2D, 
#             GL_TEXTURE_MIN_FILTER, GL_LINEAR
#         )
    
#     def gl_draw(self, texture, quads, uv):
#         w, h = texture.shape[:2]

#         glEnable(GL_TEXTURE_2D)

#         glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
#         glBindTexture(GL_TEXTURE_2D, self.texture_id)
#         glTexImage2D(
#             GL_TEXTURE_2D, 
#             0, GL_RGBA,
#             w, h,
#             0, GL_RGBA,
#             GL_UNSIGNED_BYTE,
#             texture
#         )
#         glGenerateMipmap(GL_TEXTURE_2D)

#         for quad_verts, quad_uvs in zip(quads, uv):
#             glBegin(GL_QUADS)
#             for vertex, uv in zip(quad_verts, quad_uvs):
#                 glTexCoord2f(*uv)
#                 glVertex3fv(vertex)
#             glEnd()

#         glDisable(GL_TEXTURE_2D)

#     @staticmethod
#     def to_rgba(texture):
#         dims, depth = texture.shape[:2], texture.shape[2]
#         if depth == 4:
#             return texture
#         alpha_channel = 255*np.ones((*dims, 1))
#         if depth == 3:
#             return np.concatenate(
#                 (texture, alpha_channel), 
#                 axis=-1
#             )
#         if depth == 1:
#             return np.concatenate(
#                 (*[texture]*3, alpha_channel),
#                 axis=-1
#             )
#         raise TypeError(
#             "don't know how to treat shape {} as a texture".format(texture.shape)
#         )
