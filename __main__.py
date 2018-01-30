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

    RandomPureTiler,
    Reverb,
)
from pipeline.sprite import RandomSquare


sink = PlaybackSink(
    pipeline=[
        VideoSource((640, 480)),
        RandomPureTiler([
            IdentityMosh(),
            ReverseMosh(),
            # Repack(4, '>{}f', '<{}i'),
            RandomColorspace(),
            Wordpadify(),
        ]),
        Reverb(),
    ],
)
sink.consume()
