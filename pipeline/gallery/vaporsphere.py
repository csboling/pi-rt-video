from glumpy import glm
import numpy as np

from pipeline.audio.capture import AudioSync
from pipeline.Pipeline import Pipeline
from pipeline.sprite.mesh import (
    BoxMesh,
    IcosphereMesh,
)
from pipeline.synthesis.opengl.prelude import (
    Clear,
    Rotation,
)
from pipeline.synthesis.automata.cellular import GameOfLife
from pipeline.synthesis.opengl.perspective.texture import TexturePerspective
from pipeline.synthesis.pattern import Checkerboard
from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class Vaporsphere(Pipeline):

    def __init__(self, framerate=24, resolution=None):
        source = VideoSynthesisSource(
            framerate=framerate,
            resolution=resolution
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(color=(0.7, 0.7, 0.7, 1)),
            TexturePerspective(
                # mesh=IcosphereMesh(ref_steps=2),
                mesh=BoxMesh(),
                color=AudioSync(),
                texture=GameOfLife(
                    init=np.array([
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
                        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    ]),
                    hold=3,
                ),
                # texture=Checkerboard(),
                projection=glm.perspective(45., w / h, 2., 100.),
                model=Rotation(
                    angle=lambda t: (20*t, 20*t, 20*t),
                    matrix=lambda t: np.eye(4)
                )
            ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
