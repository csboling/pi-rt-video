from glumpy import gl
import numpy as np

from pipeline.synthesis.geometry import translation_matrix
from pipeline.synthesis.opengl.shader import Shader
from pipeline.utils import params


class Perspective(Shader):
    @params(
        position=None,
        model=np.eye(4, dtype=np.float32),
        view=translation_matrix((0, 0, -5)),
        projection=np.eye(4, dtype=np.float32),
    )
    def __init__(self,
                 position,
                 model, view, projection,
                 *args, **kwargs):
        super().__init__(
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
            ''',

            attributes={
                'a_position': (3, position),
            },
            uniforms={
                'u_model': model,
                'u_view': view,
                'u_projection': projection,
            },
            *args, **kwargs
        )

    def gl_setup(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
                

