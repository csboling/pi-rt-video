from glumpy import gl
import numpy as np

from pipeline.synthesis.opengl.perspective.color import ColorPerspective
from pipeline.synthesis.opengl.shader import Snippet
from pipeline.utils import params


class TexturePerspective(ColorPerspective):
    @params(texture=None)
    def __init__(self, mesh, texture, color, *args, **kwargs):
        self.mesh = mesh
        super().__init__(
            mesh=mesh,
            color_vertex='''
            attribute vec4 a_color;
            attribute vec2 a_texcoord;
            varying vec2 v_texcoord;

            vec4 color_vertex(vec4 pos)
            {
                v_texcoord = a_texcoord;
                return a_color;
            }
            ''',
            color_fragment='''
            uniform sampler2D u_texture;
            varying vec2 v_texcoord;

            vec4 color_fragment(vec4 vertex_color)
            {
                vec4 t_color = vec4(vec3(texture2D(u_texture, v_texcoord).r), 1.0);
                return t_color * mix(vertex_color, t_color, 0.25);
            }
            ''',
            preserve_names=['v_texcoord'],
            attributes={
                'a_color': (4, color),
                'a_texcoord': (2, self.mesh.texcoord),
            },
            uniforms={
                'u_texture': lambda t: np.ascontiguousarray(texture(t)),
            },
            *args, **kwargs
        )    

    def draw(self, t):
        self.program.draw(gl.GL_TRIANGLES, self.as_index_buffer(self.mesh.faces))
