from math import *


class Emitter:
    def __init__(self, emitter_x, emitter_y):
        self._x = emitter_x
        self._y = emitter_y

    def calculate_position(self, radius, alpha, center):
        self._x = int(radius * cos(radians(alpha)) + center[0])
        self._y = int(radius * sin(radians(alpha)) + center[1])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.getter
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @y.getter
    def y(self):
        return self._y
