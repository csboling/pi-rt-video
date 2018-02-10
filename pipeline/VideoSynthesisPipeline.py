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
        source = VideoSynthesisSource(framerate=60, fill=(100, 100, 100))
        w, h = source.resolution
        super().__init__([
            source,
            Pen(
                LissajousCurve(100, 100, 3, 2),
                [
                    (148,   0, 211),
                    ( 75,   0, 130),
                    (  0,   0, 255),
                    (  0, 255,   0),
                    (255, 255,   0),
                    (255, 127,   0),
                    (255,   0,   0),
                ],
            ),
            SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PlaybackSink)
