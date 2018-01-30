from collections import deque
import operator

import cv2
import numpy as np

from pipeline.processor.pure import PureFunction


class Reverb(PureFunction):
    def __init__(self, depth=10, decay=0.5):
        self.memory = deque([0]*depth, depth)
        self.decay = decay

    def attach(self, upstream):
        super().attach(upstream)
        w, h = self.resolution
        self.acc = np.zeros((h, w, 3), dtype=np.float32)
        return self

    def __call__(self, frame):
        cv2.accumulateWeighted(frame, self.acc, self.decay)
        return cv2.convertScaleAbs(self.acc)
