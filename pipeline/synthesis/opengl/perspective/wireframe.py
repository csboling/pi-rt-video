from glumpy import gl

from pipeline.synthesis.opengl.perspective.color import UniformColorPerspective
from pipeline.utils import params


class WireframePerspective(UniformColorPerspective):

    @params(
        color=[0, 1, 0, 1],
        point_color=[0, 0, 1, 0]
    )
    def __init__(self, mesh, color, point_color, *args, **kwargs):
        self.point_color = point_color
        super().__init__(
            mesh=mesh,
            color=color,
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
        gl.glPointSize(5.0)
        self.program['u_color'] = self.point_color(t)
        self.program.draw(gl.GL_POINTS)
