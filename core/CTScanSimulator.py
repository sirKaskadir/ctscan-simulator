from math import ceil
from math import cos
from math import floor
from math import pi
from math import radians
from math import sin

import numpy as np
from bresenham import bresenham
from scipy import signal as sg
from skimage import data

from model.CTScan import CTScan


class CTScanSimulator:
    def __init__(self, image_name):
        self._sinogram = None
        self._step = 2  # TODO conf
        self._input_image = data.imread(image_name, as_grey=True)
        self._image_matrix = np.matrix(self._input_image)
        self._center = (int(floor(self._image_matrix.shape[0] / 2)), int(floor(self._image_matrix.shape[1] / 2)))
        self._radius = int(floor(min(self._image_matrix.shape[0], self._image_matrix.shape[1]) / 2))
        self._alpha = 0  # TODO conf
        self._fi = radians(250)

    def simulate(self):
        ct = CTScan()
        steps_number = int(ceil(360 / self._step)) + 1
        self._sinogram = np.empty(shape=(steps_number, ct.number_of_detectors))
        for i in range(0, steps_number - 1):
            self._alpha = i * self._step
            self._set_single_scan_coordinates(ct)
            self._do_single_scan(ct, i)

        # kernel = np.array([[1, 1, 1], [1, 1, 0], [1, 0, 0]])
        # self._sinogram = sg.convolve(self._sinogram, kernel, mode='constant')
        # self._sinogram = sg.convolve(self._sinogram, [[1.], [-1.]])
        return self._sinogram, self._radius, ct

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

    def _do_single_scan(self, ct, i):
        for j in range(0, ct.number_of_detectors - 1):
            points = list(bresenham(ct.emitter.x, ct.emitter.y, ct.detectors[j].x, ct.detectors[j].y))
            brightness_list = []
            for point in points:
                brightness = self._input_image.item(point[0] - 1, point[1] - 1)
                brightness_list.append(brightness)

            self._sinogram[i][j] = sum(brightness_list) / len(brightness_list)
