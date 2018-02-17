from functools import reduce

import numpy as np
from glumpy import glm

from pipeline.Pipeline import Pipeline
from pipeline.sprite.mesh import BoxMesh
from pipeline.synthesis.opengl.prelude import (
    Clear,
    Rotation,
)
from pipeline.synthesis.opengl.test import ColorSquare
from pipeline.synthesis.opengl.perspective import ColorPerspective
from pipeline.synthesis.pattern import (
    AnimatedColorMap,
    UniformColorMap,
    WeirdSineColorMap,
)

from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class OpenGLPipeline(Pipeline):

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=24, resolution=(320, 240)
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(),
            ColorPerspective(
                mesh=BoxMesh(),
                color=[1, 1, 0, 1],
                projection=glm.perspective(45., w / h, 2., 100.),
                model=Rotation(
                    angle=lambda t: (5*t, 0, 10*t),
                    matrix=lambda t: np.eye(4)
                )
            ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
