from pipeline.animation import CircularMotion
from pipeline.capture import VideoSource
from pipeline.playback import PlaybackSink
from pipeline.processor import Occlusion, RandomColorspace
from pipeline.sprite import RandomSquare


sink = PlaybackSink([
    VideoSource((640, 480)),
    # Occlusion(
    #     RandomSquare((10, 10)),
    #     CircularMotion((320, 240), 50)
    # ),
    RandomColorspace(),
])
sink.consume()
