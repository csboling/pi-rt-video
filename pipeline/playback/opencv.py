import cv2

from pipeline.playback.sink import Sink


class OpenCVSink(Sink):
    def consume(self):
        cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)        

        if self.save is not None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(
                self.save, fourcc, self.framerate, self.resolution)

        for frame in self.source:
            if self.save is not None:
                out.write(frame)

            cv2.imshow('window', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if self.save is not None:
            out.release()
