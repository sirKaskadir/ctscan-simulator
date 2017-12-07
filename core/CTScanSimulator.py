from math import ceil
from math import floor
from math import radians

import numpy as np
from bresenham import bresenham
from skimage import data

from config.Config import Config
from model.CTScan import CTScan


class CTScanSimulator:
    def __init__(self, image_name):
        self._sinogram = None
        self._step = Config.config["step"]
        self._input_image = data.imread(image_name, as_grey=True)
        self._image_matrix = np.matrix(self._input_image)
        self._center = (int(floor(self._image_matrix.shape[0] / 2)), int(floor(self._image_matrix.shape[1] / 2)))
        self._radius = int(floor(min(self._image_matrix.shape[0], self._image_matrix.shape[1]) / 2))
        self._alpha = Config.config["initialAlpha"]
        self._phi = radians(Config.config["phi"])

    def simulate(self):
        ct = CTScan()
        steps_number = int(ceil(Config.config["totalRotation"] / self._step)) + 1
        self._sinogram = np.empty(shape=(steps_number, ct.number_of_detectors))
        self._generate_sinogram(ct, steps_number)
        self._convolve_sinogram()
        return self._sinogram, self._radius, ct

    def _generate_sinogram(self, ct, steps_number):
        for i in range(0, steps_number - 1):
            self._alpha = i * self._step
            self._set_single_scan_coordinates(ct)
            self._do_single_scan(ct, i)

    def _convolve_sinogram(self):
        # self._sinogram = sg.convolve(self._sinogram, kernel, mode='constant')
        # self._sinogram = sg.convolve(self._sinogram, [[1.], [-1.]])
        kernel = np.array([[1, 1, 1], [1, 1, 0], [1, 0, 0]])

    def _set_single_scan_coordinates(self, ct):
        ct.emitter.calculate_position(self._radius, self._alpha, self._center)
        ct.set_detectors_coordinates_for_emitter(self._alpha, self._phi, self._radius, self._center)

    def _do_single_scan(self, ct, i):
        for j in range(0, ct.number_of_detectors - 1):
            points = list(bresenham(ct.emitter.x, ct.emitter.y, ct.detectors[j].x, ct.detectors[j].y))
            brightness_list = []
            for point in points:
                brightness = self._input_image.item(point[0] - 1, point[1] - 1)
                brightness_list.append(brightness)

            self._sinogram[i][j] = sum(brightness_list) / len(brightness_list)
