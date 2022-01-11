import operator


class Vector(tuple):
    def __new__(cls, *args):
        return tuple.__new__(cls, args)

    def __add__(self, rhs):
        return type(self)(*map(operator.__add__, self, rhs))

    def __neg__(self):
        return type(self)(*map(operator.__neg__, self))

    def __sub__(self, rhs):
        return self + -rhs
