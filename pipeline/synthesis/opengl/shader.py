from glumpy import gl, glm, gloo
import numpy as np

from pipeline.processor.Processor import TimeProcessor
from pipeline.synthesis import geometry
from pipeline.synthesis.opengl.prelude import OpenGLProcessor
from pipeline.utils import params, Parameter


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
                uniform vec4 u_color;
                attribute vec2 position;
                attribute vec4 v_color;

                void main()
                {
                    gl_Position = vec4(scale*position, 0.0, 1.0);
                    v_color = u_color;
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
                 vertex_count,
                 positions, indices,
                 model, view, projection,
                 *args, **kwargs):
        self.positions = positions
        self.indices = indices
        self.model = model
        self.view = view
        self.projection = projection

        self.gl_setup()
        
        super().__init__(gloo.Program(
            vertex='''
            uniform mat4 u_model;
            uniform mat4 u_view;
            uniform mat4 u_projection;
            uniform vec4 u_color;

            attribute vec3 a_position;

            varying vec4 v_color;

            void main()
            {
                gl_Position = u_projection *
                              u_view *
                              u_model *
                              vec4(a_position, 1.0);
                v_color = u_color;
            }
            ''',
            fragment='''
            varying vec4 v_color;

            void main()
            {
                gl_FragColor = v_color;
            }
            '''
        ), *args, **kwargs)

        self.vertex_count = vertex_count
        self.vertex_buffer = np.zeros(
            self.vertex_count,
            [
                ('a_position', np.float32, 3),
            ]
        ).view(gloo.VertexBuffer)

    def __call__(self, surface, t):
        self.load_vertex_buffers(t)
        self.index_buffer = self.indices(t).view(gloo.IndexBuffer)
        self.program.bind(self.vertex_buffer)

        self.program['u_model'] = self.model(t)
        self.program['u_view'] = self.view(t)
        self.program['u_projection'] = self.projection(t)
        self.program['u_color'] = [0, 1, 1, 1]

        return super().__call__(surface, t)

    def gl_setup(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
    
    def load_vertex_buffers(self, t):
        self.vertex_buffer['a_position'] = self.positions(t)


class MeshPerspective(Perspective):
    def __init__(self, mesh, *args, **kwargs):
        self.mesh = mesh
        positions = np.array(
            self.mesh.points
        ).astype(np.float32).reshape((-1, 3))
        super().__init__(
            vertex_count=positions.shape[0],
            positions=positions,
            indices=np.array(
                self.mesh.faces
            ).astype(np.uint32).reshape((-1,)),
            *args, **kwargs
        )

    def draw(self):
        self.program['u_color'] = [0, 1, 1, 1]
        self.program.draw(gl.GL_TRIANGLE_STRIP, self.index_buffer)

        gl.glDepthMask(gl.GL_FALSE)
        self.program['u_color'] = [1, 0, 1, 1]
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)
        for edge_row in self.mesh.edges:
            self.program.draw(gl.GL_LINE_STRIP, self.as_index_buffer(edge_row))
        gl.glDepthMask(gl.GL_TRUE)

    @staticmethod
    def as_index_buffer(points):
        return np.array(points).astype(np.uint32).view(gloo.IndexBuffer)
        
