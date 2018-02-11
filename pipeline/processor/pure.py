from abc import abstractmethod
import random

import cv2
import numpy as np

from pipeline.processor.Processor import Processor


class PureFunction(Processor):

    @abstractmethod
    def __call__(self, frame):
        pass

    def iterate(self):
        for frame in self.source:
            yield self(frame)


class Identity(PureFunction):
    def __call__(self, frame):
        return frame
            

class Lift(PureFunction):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, frame):
        return self.func(
            frame,
            *self.args, **self.kwargs
        )

class Set(PureFunction):
    def __init__(self, value):
        self.value = value
    
    def __call__(self, frame):
        return self.value

class RandomPure(PureFunction):

    def __init__(self, pure_funcs: [PureFunction], hold=3):
        self.pure_funcs = pure_funcs
        # self.hold = hold

    def __call__(self, frame):
        return random.choice(self.pure_funcs)(frame)


class CombinePure(Processor):
    def __init__(self, pure_funcs: [PureFunction]):
        self.pure_funcs = pure_funcs

    def iterate(self):
        for frame in self.source:
            yield self.combine([
                func(frame) for func in self.pure_funcs
            ])

    @abstractmethod
    def combine(self, frames):
        pass


class SliceCombine(CombinePure):
    def combine(self, frames):
        w, h = self.resolution
        ret = np.zeros((h, w, 3))
        for ix, frame in enumerate(frames):
            ret[
                :,
                int(ix*w/len(frames)):int((ix + 1)*w/len(frames)),
            ] = frame[
                :,
                int(ix*w/len(frames)):int((ix + 1)*w/len(frames)),
            ]
        return ret


class Resample(PureFunction):
    def __init__(self, factor, mode=cv2.INTER_LINEAR):
        self.factor = factor
        self.mode = mode

    @property
    def resolution(self):
        w, h = self.source.resolution
        return (int(w*self.factor), int(h*self.factor))

    def __call__(self, frame):
        return cv2.resize(frame, (0, 0), fx=self.factor, fy=self.factor)
