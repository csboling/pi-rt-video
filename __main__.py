# from pipeline.VideoProcessingPipeline import VideoProcessingPipeline
from pipeline.VideoSynthesisPipeline import VideoSynthesisPipeline
# from pipeline.OpenGLPipeline import OpenGLPipeline

# from pipeline.gallery.LissajousPlaid import LissajousPlaid


reload_on_save = False # True
trace_leaks = False

tracker = None
if trace_leaks:
    from pympler.tracker import SummaryTracker
    tracker = SummaryTracker()

p = VideoSynthesisPipeline()
# p = LissajousPlaid()
# p = OpenGLPipeline()

if reload_on_save:
    from werkzeug.serving import run_with_reloader
    run_with_reloader(p.run)
else:
    p.run()

if trace_leaks:
    tracker.print_diff()
