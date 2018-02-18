from glumpy import gl
import numpy as np

from pipeline.synthesis.opengl.perspective.color import ColorPerspective
from pipeline.utils import params


class TexturePerspective(ColorPerspective):
    @params(texture=None)
    def __init__(self, mesh, texture, *args, **kwargs):
        super().__init__(
            mesh=mesh,
            color_vertex='''
            ''',
            color_fragment='''
            ''',
            attributes={
            },
        )    
