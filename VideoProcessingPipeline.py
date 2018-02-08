import cv2
import numpy as np

from pipeline.capture import VideoSource
from pipeline.Pipeline import Pipeline
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Identity,
    Lift,
    RandomColorspace,
    RandomPureTiler,
    Repack,
    Replace,
    Reverb,
    ReverseBytes,
)


class VideoProcessingPipeline(Pipeline):
    downsampling = 4
    interpolation = cv2.INTER_NEAREST
    
    def __init__(self):
        super().__init__([
            VideoSource((656, 416)),
            Lift(
                cv2.resize,
                (0, 0), fx=1/self.downsampling, fy=1/self.downsampling,
            ),
            RandomPureTiler([
                Identity(),
                RandomColorspace(),
                Replace(br'[a-z]', br'\xca\xfe'),
                Repack(4, '<{}f', '>{}i'),
                Replace(br'[0-9]([a-z])', br'\0\0\0\0'),
            ]),
            Lift(
                cv2.resize,
                (0, 0), fx=self.downsampling, fy=self.downsampling,
                interpolation=self.interpolation,
            ),
            Reverb(),
        ])

    def run(self):
        super().run(
            lambda *args, **kwargs:
            PlaybackSink(
                *args, **kwargs,
                save='downsample{}x.avi'.format(self.downsampling)
            )
        )
        
