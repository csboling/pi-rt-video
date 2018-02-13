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

from pipeline.processor.color import RandomColorspace
from pipeline.processor.geometry import Rotate
from pipeline.processor.occlusion import Occlusion
from pipeline.processor.mosh import Repack, Replace
from pipeline.processor.pure import (
    Identity,
    Lift, 
    Set, 
    Resample,
)
from pipeline.processor.reverb import Reverb
from pipeline.processor.tiler import RandomPureTiler

from pipeline.synthesis.adapters import SurfarrayAdapter
from pipeline.synthesis.draw import (
    Fill,
    Pen,
    ROYGBIV,
)
from pipeline.synthesis.pattern import (
    AnimateMap, 
    UniformColorMap,
    WeirdSineColorMap,
)


class VideoSynthesisPipeline(Pipeline):
    downsampling = 4

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=24, fill=(100, 100, 100)
        )
        w, h = source.resolution
        x, y = (
            np.arange(-w//2, w//2)*4*2*np.pi/w, 
            np.arange(-h//2, h//2)*4*2*np.pi/h,
        )

        super().__init__([
            source,

            SurfarrayAdapter(),
            Resample(1/self.downsampling),
            AnimateMap(WeirdSineColorMap()),
            Resample(self.downsampling),
        ])

    def run(self):
        super().run(PygameSink)
