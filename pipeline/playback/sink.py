from abc import ABCMeta, abstractmethod
from functools import reduce


class Sink(metaclass=ABCMeta):

    def __init__(self, pipeline, save=None, fullscreen=True):
        self.source = reduce(
            lambda source, sink: sink.attach(source),
            pipeline
        )
        self.save = save
        self.fullscreen = fullscreen

    @property
    def resolution(self):
        return self.source.resolution

    @property
    def framerate(self):
        return self.source.framerate

    @abstractmethod
    def consume(self):
        pass
