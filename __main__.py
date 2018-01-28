from pipeline.capture import VideoSource
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,
    RandomSquare,
)


sink = PlaybackSink([
    VideoSource((640, 480)),
    Occlusion(
        RandomSquare(),
        (320, 240), (20, 20)
    ),
])
sink.consume()
