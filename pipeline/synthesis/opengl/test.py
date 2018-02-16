from glumpy import gl

from pipeline.synthesis.opengl.shader import Shader
from pipeline.utils import params


class ColorSquare(Shader):
    @params(corner_colors=None)
    def __init__(self, corner_colors):
        super().__init__(
            vertex='''
            uniform float u_scale;
            attribute vec2 a_position;
            attribute vec4 a_color;
            varying vec4 v_color;

            void main()
            {
                gl_Position = vec4(u_scale*a_position, 0.0, 1.0);
                v_color = a_color;
            } 
            """,
            fragment="""
            varying vec4 v_color;

            void main()
            {
                gl_FragColor = v_color;
            }
            ''',
            count=4,

            vertex_count=4,
            attributes={
                'a_position': (
                    2,
                    [
                        [-1,-1],
                        [-1,+1],
                        [+1,-1],
                        [+1,+1],
                    ]
                ),
                'a_color': (
                    4,
                    corner_colors,
                ),
            },
            uniforms={
                'u_scale': 1.,
            }
        )

    def draw(self, t):
        try:
            self.program.draw(gl.GL_TRIANGLE_STRIP)
        except Exception as e:
            error = gl.glGetShaderInfoLog(self.program._handle)
            lineno, mesg = self.program._parse_error(error)
            print('line {}:\n{}'.format(lineno, mesg))
