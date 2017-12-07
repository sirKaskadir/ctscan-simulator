from math import ceil
from math import cos
from math import pi
from math import radians
from math import sin

import numpy as np
from bresenham import bresenham

from model.CTScan import CTScan


class SinogramConverter:
    _sinogram = None

    def __init__(self, sinogram, radius):
        self._step = 2  # TODO conf
        self._output_image = None
        self._sinogram = sinogram
        self._sinogram_matrix = np.matrix(sinogram)
        self._radius = radius
        self._center = (radius, radius)
        self._alpha = 0  # TODO conf
        self._fi = radians(250)
        self._size = 2 * radius

    def convert(self):
        ct = CTScan()
        self._output_image = np.empty(shape=(self._size, self._size))
        steps_number = int(ceil(360 / self._step)) + 1
        for i in range(0, self._output_image.shape[0] - 1):
            for j in range(0, self._output_image.shape[1] - 1):
                self._output_image[i][j] = 0
        for i in range(0, steps_number - 1):
            self._alpha = i * self._step
            self._set_single_scan_coordinates(ct)
            self._decode_sinogram(ct, i)
        return self._output_image

    def _set_single_scan_coordinates(self, ct):
        self._set_emitter_position(ct.emitter)
        self._set_detectors_coordinates_for_emitter(ct)

    def _set_emitter_position(self, emitter):
        emitter.x = int(self._radius * cos(radians(self._alpha)) + self._center[0])
        emitter.y = int(self._radius * sin(radians(self._alpha)) + self._center[1])

    def _set_detectors_coordinates_for_emitter(self, ct):
        for i in range(0, ct.number_of_detectors - 1):
            argument = (radians(self._alpha) + pi) - (self._fi / 2) + (i * (self._fi / (ct.number_of_detectors - 1)))
            ct.detectors[i].x = int(self._radius * cos(argument)) + self._center[0]
            ct.detectors[i].y = int(self._radius * sin(argument)) + self._center[1]

    def _decode_sinogram(self, ct, i):
        for j in range(0, ct.number_of_detectors - 1):
            brightness = self._sinogram[i][j] / 255
            points = list(bresenham(ct.emitter.x, ct.emitter.y, ct.detectors[j].x, ct.detectors[j].y))
            for point in points:
                self._output_image[point[0] - 1][point[1] - 1] += brightness
