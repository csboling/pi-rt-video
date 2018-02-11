import cv2
import numpy as np

from pipeline.Pipeline import Pipeline
from pipeline.playback import PlaybackSink

from pipeline.animation import CircularMotion
from pipeline.animation.parametric import (
    LissajousCurve,
    RoseCurve,
)
from pipeline.processor.geometry import Rotate
from pipeline.processor.synthesis.adapters import SurfarrayAdapter
from pipeline.processor.synthesis.draw import (
    Fill,
    Pen,
    ROYGBIV,
)
from pipeline.processor.synthesis.source import VideoSynthesisSource
from pipeline.processor.synthesis.wireframe import (
    ProjectWireframe,
    # Rotate3D,
    Square,
)


class VideoSynthesisPipeline(Pipeline):
    def __init__(self):
        source = VideoSynthesisSource(framerate=24, fill=(100, 100, 100))
        w, h = source.resolution
        super().__init__([
            source,
            Fill((0, 0, 0)),
            ProjectWireframe(
                Square(length=300, points=20),
                # Rotate3D(lambda t: (t, 0, 0))(
                #     Square(length=100, points=20)
                # ),
                vertex_color=(255, 0, 0),
                edge_color=(0, 255, 0)
            ),
            SurfarrayAdapter(),
        ])

    def run(self):
        super().run(PlaybackSink)
