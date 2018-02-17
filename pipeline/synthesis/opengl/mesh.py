from glumpy import gl
import numpy as np

from pipeline.synthesis.opengl.perspective import Perspective


class MeshPerspective(Perspective):
    def __init__(self, mesh, *args, **kwargs):
        self.mesh = mesh
        position = np.array(
            self.mesh.points
        ).astype(np.float32).reshape((-1, 3))
        super().__init__(
            vertex_count=position.shape[0],
            position=position,
            *args, **kwargs
        )

    def draw(self, t):       
        self.program['u_color'] = [0, 1, 1, 1]
        self.program.draw(
            gl.GL_TRIANGLE_STRIP,
            self.as_index_buffer(self.mesh.faces)
        )

        gl.glDepthMask(gl.GL_FALSE)
        self.program['u_color'] = [1, 0, 1, 1]
        gl.glPointSize(3.0)
        self.program.draw(gl.GL_POINTS)
        for edge_row in self.mesh.edges:
            self.program.draw(
                gl.GL_LINE_STRIP,
                self.as_index_buffer(edge_row)
            )
        gl.glDepthMask(gl.GL_TRUE)

        
