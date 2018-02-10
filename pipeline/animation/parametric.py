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


class Harmonograph(Parametric2DMotion):
    def __init__(self, x_terms, y_terms, *args, **kwargs):
        super().__init__(
            lambda t: sum(self.term(np.cos, *params, t) for params in x_terms),
            lambda t: sum(self.term(np.sin, *params, t) for params in x_terms),
            *args, **kwargs
        )

    def term(self, func, A, f, p, d, t):
        return A*func(t * f + p)*np.exp(-d*t)


class Hypocycloid(Parametric2DMotion):
    def __init__(self, a, b, *args, **kwargs):
        super().__init__(
            lambda t: (a + b)*np.cos(t) + b*np.cos((a + b) / b * t),
            lambda t: (a + b)*np.sin(t) + b*np.sin((a + b) / b * t),
            *args, **kwargs
        )


class LissajousCurve(Parametric2DMotion):
    
    def __init__(self, A, B, a=1, b=1, delta=np.pi/2, *args, **kwargs):
        super().__init__(
            lambda t: A * np.sin(a*t + delta),
            lambda t: B * np.sin(b*t),
            *args, **kwargs
        )


class Nephroid(Parametric2DMotion):

    def __init__(self, A, B, a=3, b=3, c=3, d=3, *args, **kwargs):
        super().__init__(
            lambda t: A * (a*np.cos(t) - np.cos(b*t)),
            lambda t: B * (c*np.sin(t) - np.sin(d*t)),
            *args, **kwargs
        )


class RoseCurve(Parametric2DMotion):
    
    def __init__(self, A, B, k=1, *args, **kwargs):
        super().__init__(
            lambda t: A * np.cos(k*t) * np.cos(t),
            lambda t: B * np.cos(k*t) * np.sin(t),
            *args, **kwargs
        )
