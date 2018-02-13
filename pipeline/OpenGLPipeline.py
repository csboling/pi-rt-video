from functools import reduce

import numpy as np
from glumpy import glm, gloo

from pipeline.Pipeline import Pipeline
from pipeline.capture import VideoSource
from pipeline.sprite.wireframe import (
    SphereWireframe,
    BoxWireframe,
)
from pipeline.synthesis.opengl.prelude import (
    Clear,
    Rotation,
)
from pipeline.synthesis.opengl.shader import (
    WireframePerspective,
    ColorSquare,
)
from pipeline.synthesis.pattern import (
    AnimatedColorMap,
    UniformColorMap,
    WeirdSineColorMap,
)

from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class OpenGLPipeline(Pipeline):

    def __init__(self):
        # camera = VideoSource(resolution=(112, 112))
        # camera_frames = iter(camera)

        source = VideoSynthesisSource(
            framerate=24, resolution=(320, 240)
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(),
            WireframePerspective(
                # wireframe=BoxWireframe(width=2, height=2, depth=2),
                wireframe=SphereWireframe(r=1., density=24),
                projection=glm.perspective(45., w / h, 2., 100.),
                model=Rotation(
                    angle=lambda t: (5*t, 0, 10*t),
                    matrix=lambda t: np.eye(4)
                )
            ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
