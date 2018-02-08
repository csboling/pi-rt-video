import numpy as np

from pipeline.animation.Animation import Animation


# https://stackoverflow.com/a/13734176
def definition_to_function(s):
    lhs, rhs = s.split("=", 1)
    rhs = rhs.rstrip('; ')
    args = sympy.sympify(lhs).args
    f = sympy.sympify(rhs)
    def f_func(*passed_args):
        argdict = dict(zip(args, passed_args))
        result = f.subs(argdict)
        return float(result)
    return f_func


class Parametric2DMotion(Animation):
    
    def __init__(self, x, y, v=1.):
        self.x = x
        self.y = y
        self.v = v

    def get_xy(self, res, frame, t):
        w, h = res
        return (
            w // 2 + self.x(2*np.pi*self.v*t), 
            h // 2 + self.y(2*np.pi*self.v*t),
        )


class Lissajous(Parametric2DMotion):
    
    def __init__(self, A, B, a=1, b=1, delta=np.pi/2, *args, **kwargs):
        
        super().__init__(
            lambda t: A * np.sin(a*t + delta),
            lambda t: B * np.sin(b*t),
            *args, **kwargs
        )
