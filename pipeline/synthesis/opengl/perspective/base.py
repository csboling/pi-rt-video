from glumpy import gl, gloo
import numpy as np

from pipeline.synthesis.geometry import translation_matrix
from pipeline.synthesis.opengl.shader import Shader, Snippet
from pipeline.utils import params


class Perspective(Shader):
    @params(
        model=np.eye(4, dtype=np.float32),
        view=translation_matrix((0, 0, -5)),
        projection=np.eye(4, dtype=np.float32),
    )
    def __init__(self,
                 process_vertex, vertex, fragment,
                 position, normal,
                 model, view, projection,
                 uniforms=None, attributes=None,
                 *args, **kwargs):
        if uniforms is None:
            uniforms = dict()
        if attributes is None:
            attributes = dict()

        project = Snippet(
            process_vertex +
            '''
            uniform mat4 u_model;
            uniform mat4 u_view;
            uniform mat4 u_projection;
            attribute vec3 a_position;
            attribute vec3 a_normal;

            vec4 project()
            {
                return u_projection *
                       u_view *
                       u_model *
                       vec4(
                           process_vertex(a_position, a_normal),
                           1.0
                       );
            }
            ''',
            call='project'
        )
        projected = vertex(project())
        super().__init__(
            vertex=projected, fragment=fragment,
            attributes={
                'a_position': (3, position),
                'a_normal': (3, normal),
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
