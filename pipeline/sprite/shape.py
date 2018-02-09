from pipeline.sprite.Sprite import Sprite


class Square(Sprite):

    def __init__(self, dims, fill=lambda pos, w, h, t: (255, 255, 255)):
        self.dims = dims
        self.fill = fill

    def draw(self, frame, pos, t):
        x, y = pos
        w, h = self.dims

        frame[
            int(y):int(y)+h,
            int(x):int(x)+w,
        ] = self.fill(pos, w, h, t)
