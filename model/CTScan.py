from model.Detector import Detector
from model.Emitter import Emitter


class CTScan:

    def __init__(self):
        self._number_of_detectors = 200  # TODO add configuration for this value
        self._emitter = Emitter(0, 0)
        self._detectors = []
        for i in range(0, self._number_of_detectors - 1):
            detector = Detector(0, 0)
            self._detectors.append(detector)


    @property
    def emitter(self):
        return self._emitter

    @emitter.setter
    def emitter(self, value):
        self._emitter = value

    @emitter.getter
    def emitter(self):
        return self._emitter

    @property
    def number_of_detectors(self):
        return self._number_of_detectors

    @number_of_detectors.setter
    def number_of_detectors(self, value):
        self._number_of_detectors = value

    @number_of_detectors.getter
    def number_of_detectors(self):
        return self._number_of_detectors

    @property
    def detectors(self):
        return self._detectors

    @detectors.setter
    def detectors(self, value):
        self._detectors = value

    @detectors.getter
    def detectors(self):
        return self._detectors
