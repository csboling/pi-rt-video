from glumpy import glm
import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.sprite.mesh import IcosphereMesh
from pipeline.synthesis.opengl.prelude import Clear, Rotation
from pipeline.synthesis.opengl.perspective.ripple import (
    RipplePerspective
)
from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class Ripple(Pipeline):
    def __init__(self, framerate=24, resolution=None):
        source = VideoSynthesisSource(
            framerate=framerate,
            resolution=resolution
        )
        w, h = source.resolution

        super().__init__([
            source,

            Clear(color=(0, 0, 0, 1)),
            RipplePerspective(
                mesh=IcosphereMesh(ref_steps=2),
                projection=glm.perspective(45., w / h, 2., 100.),
                model=Rotation(
                    angle=lambda t: (20*t, 20*t, 20*t),
                    matrix=lambda t: np.eye(4)
                )
            )
        ])

    def run(self):
        super().run(OpenGLPygameSink)
