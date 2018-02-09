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
from pipeline.processor.synthesis.draw import Fill, Circle
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
            Fill((0, 0, 0)),
            SurfarrayAdapter(),
            Occlusion(
                Square(
                    (3, 3), 
                    lambda pos, w, h, t: (
                        128 + 127*np.cos(t), 
                        128 + 127*np.sin(t),
                        128 + 127*np.cos(t)*np.sin(t),
                    )
                ),
                Harmonograph(
                    [[100, 2, 3, 0.], [100, 7, 5, 0.]],
                    [[100, 13, 7, 0.], [100, 2, 11, 0.]],
                    v=0.05
                ),
                # Nephroid(25, 25, 2, 3, 3, 5, v=0.1),
            ),
            Reverb(
                depth=500, 
                decay=0.99, 
                normalize=False,
            ),
            Rotate(
                lambda t: 2*np.pi*t,
            ),
        ])

    def run(self):
        super().run(PlaybackSink)
