from glumpy import gl

from pipeline.synthesis.opengl.perspective.base import Perspective
from pipeline.synthesis.opengl.shader import Snippet
from pipeline.utils import params


class ColorPerspective(Perspective):
    def __init__(self,
                 mesh,
                 color_vertex, color_fragment,
                 process_vertex=None,
                 preserve_names=tuple(),
                 *args, **kwargs):
        self.mesh = mesh

        super().__init__(
            process_vertex=process_vertex or '''
            vec3 process_vertex(vec3 pos, vec3 normal)
            {
                return pos;
            }
            ''',
            vertex=Snippet(
                color_vertex
                +
                '''
                varying vec4 v_color;
                varying vec3 v_position;

                void draw_projection(in vec4 pos)
                {
                    gl_Position = pos;
                    v_position = pos.xyz;
                    v_color = color_vertex(pos);
                }
                ''',
                call='draw_projection',
                preserve_names=['v_color', 'v_position', *preserve_names]
            ),
            fragment=Snippet(
                color_fragment
                +
                '''
                varying vec3 v_position;
                varying vec4 v_color;

                void apply_colors()
                {
                    gl_FragColor = color_fragment(v_position, v_color);
                }
                ''',
                call='apply_colors',
                preserve_names=['v_color', 'v_position', *preserve_names]
            ),
            preserve_names=preserve_names,
            position=self.mesh.points,
            normal=self.mesh.normals,
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
    
    def draw(self, t):
        self.program.draw(
            gl.GL_TRIANGLES,
            self.as_index_buffer(self.mesh.faces)
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
            gl.GL_TRIANGLES,
            self.as_index_buffer(self.mesh.faces)
        )


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
                    0.5*(1 + sin(x*y*u_time/12)),
                    0.5*(1 + cos(x*u_time/36)),
                    0.5*(1 + sin(y*u_time/24)),
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
        split_pt = len(self.mesh.faces) // 2
        wireframe = self.mesh.faces[:split_pt]
        filled = self.mesh.faces[split_pt:]

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

        self.program.draw(
            gl.GL_TRIANGLES,
            self.as_index_buffer(self.mesh.faces)
        )
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
       
        self.program.draw(
            gl.GL_TRIANGLE_STRIP,
            self.as_index_buffer(filled)
        )
