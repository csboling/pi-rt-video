# from pipeline.VideoProcessingPipeline import VideoProcessingPipeline
# from pipeline.VideoSynthesisPipeline import VideoSynthesisPipeline
# from pipeline.OpenGLPipeline import OpenGLPipeline
from pipeline.pipelines.vaporsphere import Vaporsphere


reload_on_save = True
trace_leaks = False

tracker = None
if trace_leaks:
    from pympler.tracker import SummaryTracker
    tracker = SummaryTracker()

# p = VideoProcessingPipeline()
# p = VideoSynthesisPipeline()
# p = OpenGLPipeline()
p = Vaporsphere()

if reload_on_save:
    from werkzeug.serving import run_with_reloader
    run_with_reloader(p.run)
else:
    p.run()

if trace_leaks:
    tracker.print_diff()
