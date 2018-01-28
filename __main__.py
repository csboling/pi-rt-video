from functools import reduce
import time

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera


class VideoSource:
    def __init__(self, resolution=(640, 480)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = 30
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        time.sleep(0.1)

    @property
    def source(self):
        return self.camera.capture_continuous(
            self.raw_capture,
            format='bgr',
            use_video_port=True
        )

    def __iter__(self):
        return self.iterate()

    def iterate(self):
        for frame in self.source:
            yield frame.array
            self.raw_capture.truncate(0)


class Processor:

    def attach(self, iterator):
        self.source = iterator
        return self

    def __iter__(self):
        return self.iterate()


class GrayScaler(Processor):

    def iterate(self):
        for frame in self.source:
            yield cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def main(pipeline):
    source = reduce(
        lambda source, sink: sink.attach(source),
        pipeline
    )
    for frame in source:
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


main([
    VideoSource((640, 480)),
    GrayScaler(),
])
