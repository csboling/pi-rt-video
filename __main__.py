from pipeline.VideoProcessingPipeline import VideoProcessingPipeline
from pipeline.VideoSynthesisPipeline import VideoSynthesisPipeline

from werkzeug.serving import run_with_reloader

# p = VideoProcessingPipeline()
p = VideoSynthesisPipeline()

# p.run()
run_with_reloader(p.run)
