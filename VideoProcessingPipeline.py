from pipeline.capture import VideoSource
from pipeline.Pipeline import Pipeline
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    RandomColorspace,
    RandomPureTiler,
    Repack,
    Reverb,
    ReverseBytes,
    Wordpadify,
)


class VideoProcessingPipeline(Pipeline):
    def __init__(self):
        super().__init__([
            VideoSource((640, 480)),
            Reverb(),
            RandomPureTiler([
                ReverseBytes(),
                Repack(4, '>{}f', '<{}i'),
                Repack(4, '<{}f', '<{}i'),
                RandomColorspace(),
                Wordpadify(),
            ]),
            Reverb(),
        ])

    def run(self):
        super().run(PlaybackSink)
