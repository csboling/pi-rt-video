from abc import abstractmethod
from itertools import islice

import numpy as np

from pipeline.processor.pure import PureFunction


class Mosher(PureFunction):

    def __call__(self, frame):
        raw = frame.tobytes()
        count = len(raw)
        moshed = b''.join(self.mosh(raw))[:count]
        return np.frombuffer(
            moshed, dtype=frame.dtype
        ).reshape(
            frame.shape
        )

    @abstractmethod
    def mosh(self, in_bytes):
        pass
