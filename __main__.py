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

    RandomPureTiler
)
from pipeline.sprite import RandomSquare


sink = PlaybackSink(
    pipeline=[
        VideoSource((640, 480)),
        RandomPureTiler([
            ReverseMosh(),
            Repack(4, '>{}f', '<{}i'),
            RandomColorspace(),
            Wordpadify(),
        ]),
    ],
)
sink.consume()
