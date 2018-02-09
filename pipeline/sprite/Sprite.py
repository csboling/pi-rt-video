from abc import ABCMeta, abstractmethod


class Sprite(metaclass=ABCMeta):

    @abstractmethod
    def draw(self, frame, pos, t):
        pass
