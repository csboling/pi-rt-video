import time

from picamera.array import PiRGBArray
from picamera import PiCamera


class VideoSource:
    def __init__(self, resolution=(640, 480)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = 30
        print(self.camera.zoom)
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        time.sleep(0.1)

    @property
    def resolution(self):
        return self.camera.resolution

    @property
    def framerate(self):
        return self.camera.framerate

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
