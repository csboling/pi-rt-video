from abc import ABCMeta, abstractmethod


class Animation(metaclass=ABCMeta):

    @abstractmethod
    def get_xy(self, res, frame, t):
        pass
