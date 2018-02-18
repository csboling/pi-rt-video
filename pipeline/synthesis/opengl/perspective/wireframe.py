from glumpy import gl

from pipeline.synthesis.opengl.perspective.color import UniformColorPerspective


class WireframePerspective(UniformColorPerspective):

    def __init__(self, mesh, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color=[0, 1, 0, 1],
            *args, **kwargs
        )
    
    def draw(self, t):
        gl.glDepthMask(gl.GL_FALSE)
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)
        for edge_row in self.mesh.edges:
            self.program.draw(
                gl.GL_LINE_STRIP,
                self.as_index_buffer(edge_row)
            )
        gl.glDepthMask(gl.GL_TRUE)
