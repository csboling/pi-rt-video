from functools import reduce
from glob import glob
import os

from os.path import getmtime
import sys

import cv2

CWD = os.path.abspath(os.path.dirname(__file__))
WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in glob('{}**/*.py')]


class PlaybackSink:
    watch_period = 60

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

    def consume(self):
        cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)        

        if self.save is not None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(
                self.save, fourcc, self.framerate, self.resolution)

        watch_step = 0
        for frame in self.source:
            if self.save is not None:
                out.write(frame)

            cv2.imshow('window', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if watch_step == self.watch_period:
                watch_step = 0
                for f, mtime in WATCHED_FILES_MTIMES:
                    if getmtime(f) != mtime:
                        os.execv(sys.executable, ['python', '-m', 'pipeline'])
            else:
                watch_step += 1

        if self.save is not None:
            out.release()
