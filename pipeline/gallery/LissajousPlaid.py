import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.pygame import PygameSink

from pipeline.animation import parametric

from pipeline.processor.geometry import Rotate
from pipeline.synthesis.adapters import SurfarrayAdapter
from pipeline.synthesis.draw import (
    Fill,
    Pen,
    ROYGBIV,
)


class LissajousPlaid(Pipeline):
    downsampling = 4

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=60, fill=(100, 100, 100)
        )
        w, h = source.resolution
        x, y = (
            np.arange(-w//2, w//2)*4*2*np.pi/w, 
            np.arange(-h//2, h//2)*4*2*np.pi/h,
        )

        super().__init__([
            source,

            # Fill((0x8f, 0x8f, 0x8f, 0xff)),
            Pen(
                animation=parametric.ButterflyCurve(
                    X=30, Y=30,
                    # X=250, Y=130,
                    a=np.pi,
                    b=13,
                ),
                colors=ROYGBIV,
            ),            
            SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PygameSink)
