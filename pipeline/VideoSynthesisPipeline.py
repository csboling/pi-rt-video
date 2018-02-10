import cv2
import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.animation import CircularMotion
from pipeline.playback import PlaybackSink
from pipeline.processor.geometry import Rotate
from pipeline.processor.synthesis.source import VideoSynthesisSource
from pipeline.processor.synthesis.adapters import SurfarrayAdapter
from pipeline.processor.synthesis.draw import (
    Pen,
    ROYGBIV,
)
from pipeline.animation.parametric import (
    LissajousCurve, 
    RoseCurve,
)
from pipeline.sprite.shape import Square


class VideoSynthesisPipeline(Pipeline):
    def __init__(self):
        source = VideoSynthesisSource(framerate=24, fill=(100, 100, 100))
        w, h = source.resolution
        super().__init__([
            source,
            Pen(
                animation=RoseCurve(
                    X=100, Y=100,
                    k=np.pi,
                    v=lambda t: 0.3*np.cos(t)**2,
                ),
                colors=ROYGBIV
            ),
            SurfarrayAdapter(),
            Rotate(lambda t: 6 * np.pi * t),
        ])

    def run(self):
        super().run(PlaybackSink)
