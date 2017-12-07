from __future__ import print_function, division

import sys

import numpy as np
from PIL import Image

from core.CTScanSimulator import CTScanSimulator
from core.SinogramConverter import SinogramConverter


def do_scan():
    sinogram, radius, ct = generate_sinogram()
    img = Image.fromarray(np.uint8(sinogram * 255), 'L')
    img.save("output_sinogram.jpg")
    result = convert_sinogram(sinogram, radius)
    img2 = Image.fromarray(np.uint8(result * 255), 'L')
    img2.save("output_ct_result.jpg")


def generate_sinogram():
    simulator = CTScanSimulator(image_name=sys.argv[1])
    return simulator.simulate()


def convert_sinogram(sinogram, radius):
    converter = SinogramConverter(sinogram, radius)
    return converter.convert()


if __name__ == '__main__':
    do_scan()
