from abc import ABCMeta, abstractmethod


class Processor(metaclass=ABCMeta):

    def attach(self, upstream):
        self.source = upstream
        return self

    @property
    def framerate(self):
        return self.source.framerate

    def __iter__(self):
        return self.iterate()

    @abstractmethod
    def iterate(self):
        pass
