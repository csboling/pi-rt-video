import cv2
import numpy as np

from pipeline.animation import CircularMotion
from pipeline.capture import VideoSource
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,

    ChangeColorspace,
    RandomColorspace,
    ByteSwap,
    Wordpadify,
    RandomPure,
    SliceCombine,
)
from pipeline.sprite import RandomSquare


processors = [
    ByteSwap(4, '>{}f', '>{}i'),
    ByteSwap(4, '<{}f', '>{}i'),
    ByteSwap(8, '<{}d', '>{}Q'),
    Wordpadify(),
    *RandomColorspace.functions(),
]

sink = PlaybackSink(
    pipeline=[
        VideoSource((640, 480)),
        SliceCombine([
            RandomPure(processors),
            RandomPure(processors),
            RandomPure(processors),
            RandomPure(processors),
        ]),
    ],
)
sink.consume()
