from pipeline.Pipeline import Pipeline

# from pipeline.opengl import (
#     # OpenGLRotate,
#     OpenGLSink,
#     # OpenGLSphere,
#     # OpenGLSurfaceSource,
# )


from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class OpenGLPipeline(Pipeline):

    def __init__(self):
        # source = OpenGLSurfaceSource()
        source = VideoSynthesisSource(
            framerate=24, fill=(100, 100, 100)
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            # OpenGLCanvas(),
            # OpenGLSphere(150, points=20),
            # OpenGLRotate(lambda t: (t, 0, t)),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
