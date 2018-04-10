from glumpy import gl

from pipeline.synthesis.opengl.perspective.color import UniformColorPerspective


class WireframePerspective(UniformColorPerspective):

    def __init__(self, mesh, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color=[0, 1, 0, 1],
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
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)

