import collections
from functools import wraps
from inspect import signature


class Parameter:
    def __init__(self, values):
        self.func = self.interpret(values)

    def __call__(self, t):
        return self.func(t)

    def interpret(self, func):
        return func


class Constant(Parameter):
    def interpret(self, const):
        return lambda t: const


class Iterator(Parameter):
    def __init__(self, it, freq):
        super().__init__(it)
        self.period = 1 / freq

    def interpret(self, it):
        mark = 0
        def ret(t):
            if t >= mark:
                mark += self.period
                val = next(it)
            return val


def process_param(value):
    if isinstance(value, Parameter):
        return value
    if callable(value):
        return Parameter(value)
    # if isinstance(value, collections.Iterable):
    #     return Iterator(value)
    return Constant(value)


def params(**defaults):
    def decorate(f):
        sig = signature(f)
        @wraps(f)
        def wrapper(*args, **kwargs):
            passed_kwargs = dict()
            for name, default in defaults.items():
                value = kwargs.pop(name, default)
                if value is None:
                    raise TypeError(
                        'function {} requires an argument for {}'.format(
                            f.__name__, 
                            name 
                        )
                    )
                passed_kwargs[name] = process_param(value)
            passed_kwargs.update(kwargs)
            ba = sig.bind(*args, **passed_kwargs)
            return f(*ba.args, **ba.kwargs)
        return wrapper
    return decorate
