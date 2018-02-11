from pipeline.Pipeline import Pipeline

from pipeline.sprite.wireframe import (
    SphereWireframe,
    SquareWireframe,
)
from pipeline.synthesis.opengl import (
    BindTexture,
    Clear,
    Rotate,
)
from pipeline.synthesis.pattern import UniformColorMap, WeirdSineColorMap

from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class OpenGLPipeline(Pipeline):

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=24, resolution=(640, 480)
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(),
            BindTexture(
                wireframe=SquareWireframe(length=2.),
                texture=WeirdSineColorMap()
            ),
            Rotate(lambda t: (0.5, 0., 0.5)),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
