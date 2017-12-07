from math import *


class Detector:

    def __init__(self, detector_x, detector_y):
        self._x = detector_x
        self._y = detector_y

    def calculate_position(self, alpha, phi, radius, center, i, number_of_detectors):
        argument = (radians(alpha) + pi) - (phi / 2) + (i * (phi / (number_of_detectors - 1)))
        self._x = int(radius * cos(argument)) + center[0]
        self._y = int(radius * sin(argument)) + center[1]

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
