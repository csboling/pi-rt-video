from glumpy import gl

from pipeline.synthesis.opengl.perspective.base import Perspective
from pipeline.synthesis.opengl.shader import Snippet
from pipeline.utils import params


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
            uniforms={
                'u_color': color,
            },
            *args, **kwargs
        )       
        


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


class AnimatedColorPerspective(ColorPerspective):
    def __init__(self, mesh, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color_vertex='''
            uniform float u_time;

            vec4 color_vertex(vec4 pos)
            {
                float x = pos[0];
                float y = pos[1];
                float z = pos[2];
                return vec4(
                    sin(
                        exp(1.5*cos(u_time)) * x * y
                    ),
                    cos(
                        exp(1.5*sin(u_time)) * x
                    ),
                    sin(
                        exp(1.5*sin(u_time)) * y
                    ),
                    1.0
                );
            }
            ''',
            color_fragment='''
            vec4 color_fragment(vec4 vertex_color)
            {
                return vertex_color;
            }
            ''',
            uniforms={
                'u_time': lambda t: t,
            },
            *args, **kwargs
        )

    def draw(self, t):
        self.program.draw(
            gl.GL_TRIANGLE_STRIP,
            self.as_index_buffer(self.mesh.faces)
        )
        
        # gl.glDepthMask(gl.GL_FALSE)
        # gl.glPointSize(3.0)
        # self.program.draw(gl.GL_POINTS)
        # for edge_row in self.mesh.edges:
        #     self.program.draw(
        #         gl.GL_LINE_STRIP,
        #         self.as_index_buffer(edge_row)
        #     )
        # gl.glDepthMask(gl.GL_TRUE)
