from pipeline.processor.Processor import Processor
from pipeline.processor.color import GrayScaler, RandomColorspace
from pipeline.processor.occlusion import Occlusion


__all__ = [
    Processor,

    GrayScaler,
    RandomColorspace,

    Occlusion,
]
