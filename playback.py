from functools import reduce

import cv2


class PlaybackSink:
    def __init__(self, pipeline, save=None):
        self.source = reduce(
            lambda source, sink: sink.attach(source),
            pipeline
        )
        self.save = save

    @property
    def resolution(self):
        return self.source.resolution

    @property
    def framerate(self):
        return self.source.framerate

    def consume(self):
        if self.save is not None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(
                self.save, fourcc, self.framerate, self.resolution)

        for frame in self.source:
            if self.save is not None:
                out.write(frame)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if self.save is not None:
            out.release()
