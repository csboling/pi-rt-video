from functools import reduce

import cv2
import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opencv import OpenCVSink
from pipeline.playback.pygame import PygameSink

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
from pipeline.synthesis.pattern import (
    AnimateMap, 
    ConstantColorMap, 
    WeirdSineColorMap,
)
from pipeline.sprite.wireframe import (
    Projection2DMesh,
    Rotate3D,
    SphereWireframe,
    SquareWireframe,
    TextureMap,
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
            # AnimateMap(WeirdSineColorMap()),
            # Resample(self.downsampling),

            Fill((0, 0, 0)),
            Occlusion(
                animation=NoAnimation((w / 2, h / 2)),
                sprite=Projection2DMesh(
            #     sprite=TextureMap(
                    wireframe=reduce(
                        lambda w, f: f(w),
                        [
                            SphereWireframe(150, points=20),
                            Rotate3D(lambda t: (t, 0, t)),
                        ],
                    ),
                    vertex_color=(0, 0, 255),
                    edge_color=(0, 255, 0)
            #         texture=WeirdSineColorMap(), # ConstantColorMap(
            #         #     color=lambda t: (
            #         #         128 + int(127*np.cos(t)), 
            #         #         127 + int(127*np.sin(t)), 
            #         #         0
            #         #     )
            #         # ),
                )
            ),
            # SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PygameSink)
