from pipeline.Pipeline import Pipeline

from pipeline.sprite.wireframe import (
    SphereWireframe,
    SquareWireframe,
    CubeWireframe,
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
            framerate=24, resolution=(320, 240)
        )
        w, h = source.resolution

        super().__init__([
            source,
         
            Clear(),
            BindTexture(
                wireframe=CubeWireframe(width=2., height=2., depth=2.),
                # wireframe=SphereWireframe(r=1., density=20),
                texture=WeirdSineColorMap(),
                texture_res=(100, 100)
            ),
            Rotate(lambda t: (0.5, 0., 0.5)),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
