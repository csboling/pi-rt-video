from abc import ABCMeta, abstractmethod
import itertools

import numpy as np

from pipeline.processor.Processor import TimeProcessor


class CellularAutomaton(TimeProcessor):
    def __init__(self, init, hold=1):
        self.state = init.astype(np.uint32)
        self.rule_list = [lambda state, score: True] + self.rules()
        self.hold = hold
        self.counter = 0
        self.frame = None
        self.colors = [(255, 255, 255), (0, 0, 0)]
    
    @abstractmethod
    def score(self, state):
        pass

    @abstractmethod
    def rules(self):
        pass

    def step(self, state):
        score = self.score(state)
        next_state = np.zeros(state.shape, state.dtype)
        for value, rule in enumerate(self.rule_list):
            next_state[1:-1, 1:-1][rule(state, score)] = value
        return next_state

    def __call__(self, t): #, item, t):
        if self.frame is None or self.counter == self.hold:
            self.counter = 0
            self.frame = self.next_frame()
        else:
            self.counter += 1
        return self.frame
        # item[...] = self.frame
        # return item
        
    def next_frame(self):
        w, h = self.state.shape
        screen_w, screen_h = (100, 100) #self.resolution
        x_reps, y_reps= screen_w // w, screen_h // h
        
        colors = np.zeros((w, h, 3), np.uint8)
        for ix, color in enumerate(self.colors):
            colors[self.state == ix] = color
        self.state = self.step(self.state)
        
        return colors.repeat(y_reps, axis=0).repeat(x_reps, axis=1)

    
class GameOfLife(CellularAutomaton):
    def score(self, state):
        return sum([
            state[0:-2, 0:-2], state[0:-2, 1:-1], state[0:-2, 2:],
            state[1:-1, 0:-2],                    state[1:-1, 2:],
            state[2:,   0:-2], state[2:,   1:-1], state[2:,   2:],
        ])

    def rules(self):
        return [
            lambda state, score: (
                self.born(state, score)
                |
                self.survived(state, score)
            ),
        ]

    @staticmethod
    def born(state, score):
        return (
            (score == 3)
            &
            (state[1:-1, 1:-1] == 0)
        )

    @staticmethod
    def survived(state, score):
        return (
            ((score == 2) | (score == 3))
            &
            (state[1:-1, 1:-1] == 1)
        )
