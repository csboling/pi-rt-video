from functools import reduce

import numpy as np
from glumpy import glm

from pipeline.Pipeline import Pipeline
from pipeline.animation.parametric import RoseCurve
from pipeline.sprite.mesh import (
    BoxMesh,
    IcosphereMesh,
    MoebiusMesh,
)
from pipeline.synthesis.adapters import SurfarrayAdapter
from pipeline.synthesis.draw import TimeFuncPen, ROYGBIV
from pipeline.synthesis.geometry import translation_matrix
from pipeline.synthesis.opengl.prelude import (
    Clear,
    Rotation,
)
from pipeline.synthesis.opengl.perspective.color import (
    MultiColorPerspective,
    AnimatedColorPerspective,
)
from pipeline.synthesis.opengl.perspective.texture import TexturePerspective
from pipeline.synthesis.opengl.perspective.wireframe import WireframePerspective
from pipeline.synthesis.pattern import (
    AnimatedColorMap,
    Checkerboard,
    Constant,
    UniformColorMap,
    WeirdSineColorMap,
)

from pipeline.synthesis.source import VideoSynthesisSource
from pipeline.playback.opengl import OpenGLPygameSink


class OpenGLPipeline(Pipeline):

    def __init__(self):
        source = VideoSynthesisSource(
            framerate=24,
        )
        w, h = source.resolution
        
        adapter = SurfarrayAdapter()
        pen = TimeFuncPen(
            resolution=(256, 256),
            animation=RoseCurve(X=100, Y=100, k=np.pi),
            colors=ROYGBIV,
            fill=(1, 1, 1, 1),
        )
        
        super().__init__([
            source,
         
            Clear(color=(0.3, 0.3, 0.3, 1)),
            TexturePerspective(
                mesh=BoxMesh(),
                color=[0, 1, 1, 1],
                texture=lambda t: adapter(pen(t / 4)),
                projection=glm.perspective(45., w / h, 2., 100.),
                view=translation_matrix((0, 0, -3)),
                model=Rotation(
                    angle=lambda t: (20*t, 20*t, 20*t),
                    matrix=lambda t: np.eye(4)
                )
            ),
        ])

    def run(self):
        super().run(OpenGLPygameSink)
