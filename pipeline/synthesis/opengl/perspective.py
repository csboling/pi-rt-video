from glumpy import gl, gloo
import numpy as np

from pipeline.synthesis.geometry import translation_matrix
from pipeline.synthesis.opengl.shader import Shader, Snippet
from pipeline.utils import params


class Perspective(Shader):
    @params(
        position=None,
        model=np.eye(4, dtype=np.float32),
        view=translation_matrix((0, 0, -5)),
        projection=np.eye(4, dtype=np.float32),
    )
    def __init__(self,
                 vertex, fragment,
                 position,
                 model, view, projection,
                 uniforms=None, attributes=None,
                 *args, **kwargs):
        if uniforms is None:
            uniforms = dict()
        if attributes is None:
            attributes = dict()
        
        project = Snippet(
            '''
            uniform mat4 u_model;
            uniform mat4 u_view;
            uniform mat4 u_projection;
            attribute vec3 a_position;

            vec4 project()
            {
                return u_projection *
                       u_view *
                       u_model *
                       vec4(a_position, 1.0);
            }
            ''',
            default='project'
        )
        projected = vertex(project())
        super().__init__(
            vertex=projected, fragment=fragment,
            attributes={
                'a_position': (3, position),
                **attributes,
            },
            uniforms={
                'u_model': model,
                'u_view': view,
                'u_projection': projection,
                **uniforms,
            },
            *args, **kwargs
        )

    def gl_setup(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
                

class ColorPerspective(Perspective):
    def __init__(self,
                 mesh,
                 color_vertex, color_fragment,
                 *args, **kwargs):
        self.mesh = mesh

        super().__init__(
            vertex=Snippet(
                color_vertex
                +
                '''
                varying vec4 v_color;

                void draw_projection(in vec4 pos)
                {
                    gl_Position = pos;
                    v_color = color_vertex(pos);
                }
                ''',
                call='draw_projection',
                preserve_names=['v_color']
            ),
            fragment=Snippet(
                color_fragment
                +
                '''
                varying vec4 v_color;

                void apply_colors()
                {
                    gl_FragColor = color_fragment(v_color);
                }
                ''',
                call='apply_colors',
                preserve_names=['v_color']
            ),
            position=self.mesh.points,
            vertex_count=len(self.mesh.points),
            *args, **kwargs
        )

class UniformColorPerspective(ColorPerspective):
    @params(color=None)
    def __init__(self, mesh, color, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color_vertex='''
            uniform vec4 u_color;

            vec4 color_vertex(vec4 pos)
            {
                return u_color;
            }
            ''',
            color_fragment='''
            vec4 color_fragment(vec4 vertex_color)
            {
                return vertex_color;
            }
            ''',
            *args, **kwargs
        )

    def draw(self, t):       
        self.program['u_color'] = [0, 1, 1, 1]
        self.program.draw(
            gl.GL_TRIANGLE_STRIP,
            self.as_index_buffer(self.mesh.faces)
        )

        gl.glDepthMask(gl.GL_FALSE)
        self.program['u_color'] = [1, 0, 1, 1]
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)
        for edge_row in self.mesh.edges:
            self.program.draw(
                gl.GL_LINE_STRIP,
                self.as_index_buffer(edge_row)
            )
        gl.glDepthMask(gl.GL_TRUE)


class MultiColorPerspective(ColorPerspective):
    @params(color=None)
    def __init__(self, mesh, color, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color_vertex='''
            attribute vec4 a_color;

            vec4 color_vertex(vec4 pos)
            {
                return a_color;
            }
            ''',
            color_fragment='''
            vec4 color_fragment(vec4 vertex_color)
            {
                return vertex_color;
            }
            ''',
            attributes={
                'a_color': (4, color),
            },
            *args, **kwargs
        )
       
    def draw(self, t):
        self.program.draw(
            gl.GL_TRIANGLE_STRIP,
            self.as_index_buffer(self.mesh.faces)
        )
        
        gl.glDepthMask(gl.GL_FALSE)
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)
        for edge_row in self.mesh.edges:
            self.program.draw(
                gl.GL_LINE_STRIP,
                self.as_index_buffer(edge_row)
            )
        gl.glDepthMask(gl.GL_TRUE)
