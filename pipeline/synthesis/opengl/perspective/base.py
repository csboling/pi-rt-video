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

    def gl_setup(self, t):
        super().gl_setup(t)
        gl.glEnable(gl.GL_DEPTH_TEST)

    def gl_teardown(self, t):
        gl.glDisable(gl.GL_DEPTH_TEST)
        super().gl_teardown(t)
