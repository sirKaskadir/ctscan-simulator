import sys

from core.CTScanSimulator import CTScanSimulator

from core.SinogramConverter import SinogramConverter


def do_scan():
    sinogram = generate_sinogram()
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
