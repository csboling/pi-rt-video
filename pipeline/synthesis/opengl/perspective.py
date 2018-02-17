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
    @params(color=None)
    def __init__(self, mesh, color, *args, **kwargs):
        self.mesh = mesh
        position = np.array(
            self.mesh.points
        ).astype(np.float32).reshape((-1, 3))

        super().__init__(
            vertex=Snippet(
                '''
                uniform vec4 u_color;
                varying vec4 v_color;
                
                void draw_projection(in vec4 pos)
                {
                    gl_Position = pos;
                    v_color = u_color;
                }
                ''',
                preserve_names=['v_color']
            ),
            fragment=Snippet(
                '''
                varying vec4 v_color;

                void color_fragments()
                {
                    gl_FragColor = v_color;
                }
                ''',
                preserve_names=['v_color']
            ),
            position=position,
            vertex_count=position.shape[0],
            uniforms={
                'u_color': color,
            },
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

