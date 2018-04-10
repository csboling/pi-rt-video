reload_on_save = False
trace_leaks = False

tracker = None
if trace_leaks:
    from pympler.tracker import SummaryTracker
    tracker = SummaryTracker()

resolution = (640, 480)

# ordered from least to most demanding, library-wise

# pygame
from pipeline.gallery.lissajous_plaid import LissajousPlaid
p = LissajousPlaid(resolution=resolution)

# opengl, glumpy
# from pipeline.gallery.vaporsphere import Vaporsphere
# p = Vaporsphere(resolution=resolution)

# pyo for audio capture
# p = AudioCheckerTwitch(resolution=resolution)
# from pipeline.gallery.audio_checker_twitch import AudioCheckerTwitch

if reload_on_save:
    from werkzeug.serving import run_with_reloader
    run_with_reloader(p.run)
else:
    p.run()

if trace_leaks:
    tracker.print_diff()
