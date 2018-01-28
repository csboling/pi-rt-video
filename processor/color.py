import cv2

from pipeline.processor.Processor import Processor


class GrayScaler(Processor):

    def iterate(self):
        for frame in self.source:
            yield cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
