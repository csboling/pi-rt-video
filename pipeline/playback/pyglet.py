import pyglet

from pipeline.playback.sink import Sink


class PygletSink(Sink):
    def consume(self):
        window = pyglet.window.Window()
        label = pyglet.text.Label(
            'Hello, world',
            font_name='Times New Roman',
            font_size=36,
            x=window.width//2, y=window.height//2,
            anchor_x='center', anchor_y='center'
        )
        
        it = iter(self.source)

        @window.event
        def on_draw():
            window.clear()
            frame = next(it)
            img = pyglet.image.ImageData(*self.resolution, 'RGB', frame.tobytes())
            img.blit(0, 0)

        pyglet.app.run()
