from math import ceil
from math import radians

import numpy as np
from bresenham import bresenham

from config.Config import Config
from model.CTScan import CTScan


class SinogramConverter:
    _sinogram = None

    def __init__(self, sinogram, radius):
        self._step = Config.config["step"]
        self._output_image = None
        self._sinogram = sinogram
        self._sinogram_matrix = np.matrix(sinogram)
        self._radius = radius
        self._center = (radius, radius)
        self._alpha = Config.config["initialAlpha"]
        self._phi = radians(Config.config["phi"])
        self._size = 2 * radius

    def convert(self):
        ct = CTScan()
        self._output_image = np.empty(shape=(self._size, self._size))
        steps_number = int(ceil(Config.config["totalRotation"] / self._step)) + 1
        self._initialize_output_image()
        self._reconstruct_from_sinogram(ct, steps_number)
        return self._output_image

    def _reconstruct_from_sinogram(self, ct, steps_number):
        for i in range(0, steps_number - 1):
            self._alpha = i * self._step
            self._set_single_scan_coordinates(ct)
            self._reconstruct_single_sinogram_slice(ct, i)

    def _initialize_output_image(self):
        for i in range(0, self._output_image.shape[0] - 1):
            for j in range(0, self._output_image.shape[1] - 1):
                self._output_image[i][j] = 0

    def _set_single_scan_coordinates(self, ct):
        ct.emitter.calculate_position(self._radius, self._alpha, self._center)
        ct.set_detectors_coordinates_for_emitter(self._alpha, self._phi, self._radius, self._center)

    def _reconstruct_single_sinogram_slice(self, ct, i):
        for j in range(0, ct.number_of_detectors - 1):
            brightness = self._sinogram[i][j] / 255
            points = list(bresenham(ct.emitter.x, ct.emitter.y, ct.detectors[j].x, ct.detectors[j].y))
            for point in points:
                self._output_image[point[0] - 1][point[1] - 1] += brightness
