from functools import reduce

import numpy as np
from glumpy import glm, gloo

from pipeline.Pipeline import Pipeline
from pipeline.capture import VideoSource
from pipeline.sprite.wireframe import (
    SphereWireframe,
    SquareWireframe,
    CubeWireframe,
    Rotate3D,
)
from pipeline.synthesis.opengl import (
    WireframePerspective,
    Clear,
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
        camera = VideoSource(resolution=(112, 112))
        camera_frames = iter(camera)

        source = VideoSynthesisSource(
            framerate=24,
        )
        w, h = source.resolution


        super().__init__([
            source,
         
            Clear(),
            ColorSquare(corner_colors=lambda t: [
                [np.cos(t), 0,         0,                   1],
                [0,         np.sin(1), 0,                   1],
                [0,         0,         np.cos(1)*np.sin(t), 1],
                [np.cos(t) + np.sin(t), np.cos(t) - np.sin(t), 0,                   1],
            ]),
            
            # WireframePerspective(
            #     wireframe=CubeWireframe(width=2, height=2, depth=2),
            #     projection=glm.perspective(45., w / h, 2., 100.),
            # ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
