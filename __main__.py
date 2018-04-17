reload_on_save = False  # hangs on windows
trace_leaks = False

tracker = None
if trace_leaks:
    from pympler.tracker import SummaryTracker
    tracker = SummaryTracker()

resolution = (800, 800)

# ordered from least to most demanding, library-wise

# pygame
# from pipeline.gallery.lissajous_plaid import LissajousPlaid
# p = LissajousPlaid(resolution=resolution)

# opengl, glumpy
# from pipeline.gallery.vaporsphere import Vaporsphere
# p = Vaporsphere(resolution=resolution)

# pyo for audio capture
# from pipeline.gallery.audio_checker_twitch import AudioCheckerTwitch
# p = AudioCheckerTwitch(resolution=resolution)

from pipeline.gallery.ripple import Ripple
p = Ripple()

if reload_on_save:
    from werkzeug.serving import run_with_reloader
    run_with_reloader(p.run)
else:
    p.run()

if trace_leaks:
    tracker.print_diff()
