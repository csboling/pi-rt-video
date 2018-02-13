from abc import ABCMeta, abstractmethod


class Processor(metaclass=ABCMeta):

    def attach(self, upstream):
        self.source = upstream
        return self

    @property
    def resolution(self):
        return self.source.resolution

    @property
    def framerate(self):
        return self.source.framerate

    def __iter__(self):
        return self.iterate()

    @abstractmethod
    def iterate(self):
        pass


class TimeProcessor(Processor):

    def iterate(self):
        t = 0
        for item in self.source:
            self(item, t)
            yield item
            t += 1 / self.framerate

    @abstractmethod
    def __call__(self, item, t):
        pass
        
