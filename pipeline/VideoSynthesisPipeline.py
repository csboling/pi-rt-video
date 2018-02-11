from functools import reduce

import cv2
import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback import PlaybackSink

from pipeline.animation.Animation import NoAnimation
from pipeline.animation import CircularMotion
from pipeline.animation.parametric import (
    LissajousCurve,
    RoseCurve,
)
from pipeline.processor.geometry import Rotate
from pipeline.processor.occlusion import Occlusion

from pipeline.processor.mosh import Repack, Replace
from pipeline.processor.pure import Lift, Set, Resample

from pipeline.synthesis.adapters import SurfarrayAdapter
from pipeline.synthesis.draw import (
    Fill,
    Pen,
    ROYGBIV,
)
from pipeline.synthesis.pattern import FunkySineThing
from pipeline.sprite.wireframe import (
    Projection2DMesh,
    Rotate3D,
    SphereWireframe,
    SquareWireframe,
)


class VideoSynthesisPipeline(Pipeline):
    downsampling = 4

    def __init__(self):
        source = VideoSynthesisSource(framerate=24, fill=(100, 100, 100))
        w, h = source.resolution
        x, y = (
            np.arange(-w//2, w//2)*4*2*np.pi/w, 
            np.arange(-h//2, h//2)*4*2*np.pi/h,
        )

        super().__init__([
            source,

            # SurfarrayAdapter(),
            # Resample(1/self.downsampling),
            # FunkySineThing(),
            # Resample(self.downsampling),

            Fill((0, 0, 0)),
            Occlusion(
                animation=NoAnimation((w / 2, h / 2)),
                sprite=Projection2DMesh(
                    reduce(
                        lambda w, f: f(w),
                        [
                            SphereWireframe(150, points=20),
                            # SquareWireframe(length=300, points=20),
                            Rotate3D(lambda t: (t, 0, t)),
                        ]
                    ),
                    vertex_color=(255, 0, 0),
                    edge_color=(0, 255, 0)
                )
            ),
            SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PlaybackSink)
