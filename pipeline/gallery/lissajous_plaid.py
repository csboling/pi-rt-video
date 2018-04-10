import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.pygame import PygameSink

from pipeline.animation import parametric

from pipeline.synthesis.adapters import SurfarrayAdapter
from pipeline.synthesis.draw import (
    Pen,
    ROYGBIV,
)


class LissajousPlaid(Pipeline):
    downsampling = 4

    def __init__(self, resolution=None):
        source = VideoSynthesisSource(
            framerate=60,
            fill=(100, 100, 100),
            resolution=resolution
        )
        w, h = source.resolution

        super().__init__([
            source,

            # Fill((0x8f, 0x8f, 0x8f, 0xff)),
            Pen(
                animation=parametric.LissajousCurve(
                    X=0.5*w, Y=0.5*h,
                    a=np.pi,
                    b=13,
                ),
                colors=ROYGBIV,
            ),
            SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PygameSink)
