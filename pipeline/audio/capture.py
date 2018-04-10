from pyo import (
    Input,
    Server,
)


class AudioSync:
    def __init__(self):
        self.server = Server(
            ichnls=1,
            winhost='mme'
        ).boot()
        self.server.start()
        self.mic = Input()

    def __call__(self, t):
        value = self.mic.get()
        return (
            int(128 + 127*value),
            int(128 + 127*value),
        )
