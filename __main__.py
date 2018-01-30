import cv2
import numpy as np

from pipeline.animation import CircularMotion
from pipeline.capture import VideoSource
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,

    ChangeColorspace,
    RandomColorspace,

    Repack,
    MangleBytes,
    IdentityMosh,
    ReverseMosh,
    Wordpadify,

    Lift,
    RandomPure,
    SliceCombine,
)
from pipeline.sprite import RandomSquare


sink = PlaybackSink(
    pipeline=[
        VideoSource((640, 480)),
        Lift(cv2.erode, kernel=np.ones((5, 5)), iterations=1),
        # MangleBytes(moshers),
        # SliceCombine([])
        # RandomColorspace(),
        # RandomPure([]),
    ],
)
sink.consume()
