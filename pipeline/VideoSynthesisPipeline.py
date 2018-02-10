import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.animation import CircularMotion
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,
    Reverb,
)
from pipeline.processor.geometry import Rotate
from pipeline.processor.synthesis.source import VideoSynthesisSource
from pipeline.processor.synthesis.draw import (
    Circle,
    Fill,
    Pen,
)
from pipeline.processor.synthesis.adapters import SurfarrayAdapter
from pipeline.animation.parametric import (
    Harmonograph,
    Hypocycloid,
    LissajousCurve, 
    Nephroid,
    RoseCurve,
)
from pipeline.sprite.shape import Square


class VideoSynthesisPipeline(Pipeline):
    def __init__(self):
        source = VideoSynthesisSource()
        w, h = source.resolution
        super().__init__([
            source,
            Pen(
                Harmonograph(
                    [[100, 2, 1, 0.05], [100, 3, 1, 0.05]],
                    [[100, 3, 1, 0.05], [100, 1, 1, 0.05]],

                    v=0.05
                ),
                lambda pos, w, h, t: (
                    0, 255, 0,
                ),
            ),
            SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PlaybackSink)
