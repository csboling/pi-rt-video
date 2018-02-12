# from pipeline.VideoProcessingPipeline import VideoProcessingPipeline
from pipeline.VideoSynthesisPipeline import VideoSynthesisPipeline
from pipeline.OpenGLPipeline import OpenGLPipeline

from werkzeug.serving import run_with_reloader

# p = VideoProcessingPipeline()
# p = VideoSynthesisPipeline()
p = OpenGLPipeline()

p.run()
# run_with_reloader(p.run)
