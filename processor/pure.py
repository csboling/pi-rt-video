from abc import abstractmethod
import random

import numpy as np

from pipeline.processor.Processor import Processor


class PureFunction(Processor):

    @abstractmethod
    def __call__(self, frame):
        pass

    def iterate(self):
        for frame in self.source:
            yield self(frame)


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


class RandomPure(PureFunction):

    def __init__(self, pure_funcs: [PureFunction], hold=3):
        self.pure_funcs = pure_funcs
        # self.hold = hold

    def __call__(self, frame):
        return random.choice(self.pure_funcs)(frame)

    # def iterate(self):
    #     it = iter(self.source)
    #     while True:
    #         func = random.choice(self.pure_funcs)
    #         hold = random.randint(1, self.hold)
    #         for _ in range(hold):
    #             yield func(next(it))


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
