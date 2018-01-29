import cv2

from pipeline.animation import CircularMotion
from pipeline.capture import VideoSource
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,
    ChangeColorspace,
    RandomColorspace
)
from pipeline.sprite import RandomSquare


sink = PlaybackSink(
    pipeline=[
        VideoSource((640, 480)),
        # Occlusion(
        #     RandomSquare((10, 10)),
        #     CircularMotion((320, 240), 50)
        # ),
        RandomColorspace(),
    ],
    save='random_colorspaces.avi'
)
sink.consume()
