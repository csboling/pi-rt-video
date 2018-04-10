from pyo import (
    Follower,
    Input,
    Server,
)


class AudioSync:
    def __init__(self):
        self.server = Server(ichnls=1).boot()
        self.server.start()
        self.mic = Input()
        while True:
            print(self.mic.get())

    def __call__(self, t):
        pass
