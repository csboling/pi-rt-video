from abc import ABCMeta, abstractmethod


class Animation(metaclass=ABCMeta):

    @abstractmethod
    def get_xy(self, res, frame, t):
        pass


class NoAnimation(Animation):

    def __init__(self, pos):
        self.pos = pos

    def get_xy(self, *args, **kwargs):
        return self.pos
