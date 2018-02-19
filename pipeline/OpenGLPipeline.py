from functools import reduce

import numpy as np
from glumpy import glm

from pipeline.Pipeline import Pipeline
from pipeline.sprite.mesh import (
    BoxMesh,
    IcosphereMesh,
    MoebiusMesh,
)
from pipeline.synthesis.geometry import translation_matrix
from pipeline.synthesis.opengl.prelude import (
    Clear,
    Rotation,
)
from pipeline.synthesis.opengl.perspective.color import (
    MultiColorPerspective,
    AnimatedColorPerspective,
)
from pipeline.synthesis.opengl.perspective.texture import TexturePerspective
from pipeline.synthesis.opengl.perspective.wireframe import WireframePerspective
from pipeline.synthesis.pattern import (
    AnimatedColorMap,
    Checkerboard,
    UniformColorMap,
    WeirdSineColorMap,
)

from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class OpenGLPipeline(Pipeline):

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=24,
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(color=(1, 0, 1, 1)),
            TexturePerspective(
                mesh=IcosphereMesh(ref_steps=2),
                color=[0, 1, 1, 1],
                texture=Checkerboard(),
                projection=glm.perspective(45., w / h, 2., 100.),
                model=Rotation(
                    angle=lambda t: (20*t, 20*t, 20*t),
                    matrix=lambda t: np.eye(4)
                )
            ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
