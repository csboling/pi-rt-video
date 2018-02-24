import numpy as np

from pipeline.animation.Animation import Animation
from pipeline.utils import params


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

    @params(v=1)
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.v = v

    def get_xy(self, res, frame, t):
        w, h = res
        return (
            w // 2 + self.x(2*np.pi*self.v(t)*t), 
            h // 2 + self.y(2*np.pi*self.v(t)*t),
        )


class Harmonograph(Parametric2DMotion):
    def __init__(self, x_terms, y_terms, *args, **kwargs):
        super().__init__(
            lambda t: sum(self.term(np.cos, **params, t=t) for params in x_terms),
            lambda t: sum(self.term(np.sin, **params, t=t) for params in y_terms),
            *args, **kwargs
        )

    @params(A=None, f=1, p=0, d=0)
    def term(self, func, A, f, p, d, t):
        return A(t)*func(t * f(t) + p(t))*np.exp(-d(t)*t)


class Hypocycloid(Parametric2DMotion):
    @params(X=None, Y=None, a=1, b=1)
    def __init__(self, X, Y, a, b, *args, **kwargs):
        super().__init__(
            lambda t: X(t) * (
                (a(t) + b(t))*np.cos(t) 
                + 
                b(t)*np.cos(
                    (a(t) + b(t)) / b(t) * t
                )
            ),
            lambda t: Y(t) * (
                (a(t) + b(t))*np.sin(t) 
                + 
                b(t)*np.sin(
                    (a(t) + b(t)) / b(t) * t
                )
            ),
            *args, **kwargs
        )


class LissajousCurve(Parametric2DMotion):
    
    @params(X=None, Y=None, a=1, b=1, delta=np.pi/2)
    def __init__(self, X, Y, a, b, delta, *args, **kwargs): 
        super().__init__(
            lambda t: X(t) * np.sin(a(t)*t / 4 + delta(t)),
            lambda t: Y(t) * np.sin(b(t)*t / 4),
            *args, **kwargs
        )


class Nephroid(Parametric2DMotion):

    @params(X=None, Y=None, a=3, b=3, c=3, d=3)
    def __init__(self, X, Y, a, b, c, d, *args, **kwargs):
        super().__init__(
            lambda t: X(t) * (a(t)*np.cos(t) - np.cos(b(t)*t)),
            lambda t: Y(t) * (c(t)*np.sin(t) - np.sin(d(t)*t)),
            *args, **kwargs
        )


class RoseCurve(Parametric2DMotion):
    
    @params(X=None, Y=None, k=1)
    def __init__(self, X, Y, k, *args, **kwargs):
        super().__init__(
            lambda t: X(t) * np.cos(k(t)*t) * np.cos(t),  
            lambda t: Y(t) * np.cos(k(t)*t) * np.sin(t),
            *args, **kwargs
        )

class ButterflyCurve(Parametric2DMotion):

    @params(X=None, Y=None, a=4, b=12)
    def __init__(self, X, Y, a, b, *args, **kwargs):
        super().__init__(
            lambda t: X(t) * np.sin(t) * (
                np.exp(np.cos(t))
                -
                2*np.cos(a(t) * t)
                - (np.sin(t / b(t)))**5
            ),
            lambda t: Y(t) * np.cos(t) * (
                np.exp(np.cos(t))
                -
                2*np.cos(a(t) * t)
                - (np.sin(t / b(t)))**5
            ),
            *args, **kwargs
        )
