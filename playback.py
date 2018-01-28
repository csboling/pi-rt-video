from functools import reduce

import cv2


class PlaybackSink:
    def __init__(self, pipeline):
        self.source = reduce(
            lambda source, sink: sink.attach(source),
            pipeline
        )

    @property
    def framerate(self):
        return self.source.framerate

    def consume(self):
        for frame in self.source:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
