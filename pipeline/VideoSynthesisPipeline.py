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
    Harmonograph,
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
from pipeline.synthesis.automata.cellular import GameOfLife


class VideoSynthesisPipeline(Pipeline):
    downsampling = 4

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=24, resolution=(320, 240), #, fill=(100, 100, 100)
        )
        w, h = source.resolution
        x, y = (
            np.arange(-w//2, w//2)*4*2*np.pi/w, 
            np.arange(-h//2, h//2)*4*2*np.pi/h,
        )

        super().__init__([
            source,
            SurfarrayAdapter(),
            GameOfLife(
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
        ])

    def run(self):
        super().run(PygameSink)
