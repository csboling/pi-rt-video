from functools import reduce

import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.capture import VideoSource
from pipeline.sprite.wireframe import (
    SphereWireframe,
    SquareWireframe,
    CubeWireframe,
    Rotate3D,
)
from pipeline.synthesis.opengl import (
    BindTexture,
    Clear,
    Rotate,
    TexturedSphere,
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
        camera = VideoSource(resolution=(112, 112))
        camera_frames = iter(camera)

        source = VideoSynthesisSource(
            framerate=24, resolution=(320, 240)
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(),
            Rotate(lambda t: (1., 0., 0.5)),
            TexturedSphere(
                texture=WeirdSineColorMap()
            ),
            # BindTexture(
            #     wireframe=CubeWireframe(),
            #     texture=WeirdSineColorMap(),
            # ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
