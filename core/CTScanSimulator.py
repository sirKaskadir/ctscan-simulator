from math import floor
from math import ceil
from math import cos
from math import sin
from math import radians
from math import pi

from matplotlib import pyplot as plt
from skimage import data
import numpy as np

from model.CTScan import CTScan


class CTScanSimulator:

    def __init__(self, image_name):
        self._sinogram = None
        self._step = 4  # TODO conf
        self._input_image = data.imread(image_name, as_grey=True)
        self._image_matrix = np.matrix(self._input_image)
        self._center = (int(floor(self._image_matrix.shape[0] / 2)), int(floor(self._image_matrix.shape[1] / 2)))
        self._radius = int(floor(min(self._image_matrix.shape[0], self._image_matrix.shape[1]) / 2))
        self._alpha = 0  # TODO conf
        self._fi = 180
        plt.imshow(self._input_image, cmap=plt.gray())

    def simulate(self):
        ct = CTScan()
        steps_number = int(ceil(360 / self._step)) + 1
        self._sinogram = np.empty([ct.number_of_detectors, steps_number])
        for i in range(0, steps_number - 1):
            self._alpha = i * self._step
            self._set_single_scan_coordinates(ct)
            self._do_single_scan(ct)

        # plt.show()  # FIXME tmp
        return self._sinogram

    def _set_single_scan_coordinates(self, ct):
        self._set_emitter_position(ct.emitter)
        self._set_detectors_coordinates_for_emitter(ct)

    def _set_emitter_position(self, emitter):
        emitter.x = self._radius * cos(radians(self._alpha)) + self._center[0]
        emitter.y = self._radius * sin(radians(self._alpha)) + self._center[1]

    def _set_detectors_coordinates_for_emitter(self, ct):
        for i in range(0, ct.number_of_detectors - 1):
            argument = (self._alpha + pi) - (self._fi / 2) + (i * (self._fi / (ct.number_of_detectors - 1)))
            ct.detectors[i].x = self._radius * cos(radians(argument)) + self._center[0]
            ct.detectors[i].y = self._radius * sin(radians(argument)) + self._center[1]

    def _do_single_scan(self, ct):
        print(self._sinogram.shape)
