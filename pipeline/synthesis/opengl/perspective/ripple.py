from glumpy import gl

from pipeline.synthesis.opengl.perspective.color import ColorPerspective
from pipeline.utils import params


class RipplePerspective(ColorPerspective):
    @params(color=[0, 1, 0, 1])
    def __init__(self, mesh, color, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color_vertex='''
            #extension GL_OES_standard_derivatives : enable
            precision highp float;

            uniform vec4 u_color;

            vec4 color_vertex(vec4 pos)
            {
                return u_color;
            }
            ''',
            process_vertex='''
            uniform float u_time;
            const float amplitude = 0.125;
            const float frequency = 4;
            const float PI = 3.14159;
            varying vec3 v_normal;

            vec3 process_vertex(vec3 pos, vec3 normal)
            {
                v_normal = normal;
                float distance = pos.x * pos.y * pos.z;
                float deformation = amplitude*sin(-PI*distance*frequency + u_time);
                return pos + deformation * normal;
            }
            ''',
            color_fragment='''
            varying vec3 v_normal;

            vec4 color_fragment(vec3 position, vec4 vertex_color)
            {
                vec3 surfaceToLight = vec3(2.0, -2.0, 0.0) - position;
                float brightness = dot(v_normal, surfaceToLight) /
                      (length(surfaceToLight) * length(v_normal));
                brightness = max(min(brightness, 1.0), 0.0);
            return vec4(v_normal, 1.0) * (0.1 + 0.9 * brightness);
            }
            ''',
            uniforms={
                'u_color': color,
                'u_time': lambda t: t,
            },
            preserve_names=['v_normal'],
            *args, **kwargs
        )

    def gl_setup(self, t):
        super().gl_setup(t)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

    def gl_teardown(self, t):
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        super().gl_teardown(t)

    def draw(self, t):
        self.program.draw(
            gl.GL_TRIANGLES,
            self.as_index_buffer(self.mesh.faces)
        )
