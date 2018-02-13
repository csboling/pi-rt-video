import time

from picamera.array import PiRGBArray
from picamera import PiCamera


class CameraSource:
    def __init__(self, resolution=(640, 480), framerate=30):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        print(self.camera.zoom)
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        time.sleep(0.1)
        self.source = self.camera.capture_continuous(
            self.raw_capture,
            format='bgr',
            use_video_port=True
        )

    @property
    def resolution(self):
        return self.camera.resolution

    @property
    def framerate(self):
        return self.camera.framerate

    def __iter__(self):
        return self.iterate()

    def iterate(self):
        for frame in self.source:
            yield frame.array
            self.raw_capture.truncate(0)
            self.raw_capture.seek(0)
