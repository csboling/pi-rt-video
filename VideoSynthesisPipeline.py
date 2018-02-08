from pipeline.Pipeline import Pipeline
from pipeline.animation import CircularMotion
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,
    Reverb,
)
from pipeline.processor.synthesis.source import VideoSynthesisSource
from pipeline.processor.synthesis.draw import Fill, Circle
from pipeline.processor.synthesis.adapters import SurfarrayAdapter


class VideoSynthesisPipeline(Pipeline):
    def __init__(self):
        source = VideoSynthesisSource()
        w, h = source.resolution
        super().__init__([
            source,
            Fill((0, 0, 0)),
            Occlusion(
                Circle(10, (0, 255, 0)),
                CircularMotion((w // 2, h // 2), 50)
            ),
            SurfarrayAdapter(),
            Reverb(),
        ])

    def run(self):
        super().run(PlaybackSink)
