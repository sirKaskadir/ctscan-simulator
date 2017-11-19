import sys
from skimage import io, img_as_uint, exposure

from core.CTScanSimulator import CTScanSimulator

from core.SinogramConverter import SinogramConverter

from matplotlib import pyplot as plt


def do_scan():
    sinogram = generate_sinogram()
    exposure.rescale_intensity(sinogram, out_range='float')
    sinogram = img_as_uint(sinogram)
    io.imsave("output.jpg", sinogram)
    result = convert_sinogram(sinogram)
    print_result(result)


def generate_sinogram():
    simulator = CTScanSimulator(image_name=sys.argv[1])
    return simulator.simulate()


def print_result(result):
    print(result)


def convert_sinogram(sinogram):
    converter = SinogramConverter()
    return "some image"


if __name__ == '__main__':
    do_scan()
