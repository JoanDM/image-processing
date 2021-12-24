import os
from pathlib import Path

import cv2

_base_dir = os.path.abspath(os.path.dirname(__file__))
_base_dir_pathlib = Path(_base_dir)
_results_dir_pathlib = Path(_base_dir) / "results"
_resources_dir_pathlib = Path(_base_dir) / "resources"
_tmp_dir_pathlib = _results_dir_pathlib / "tmp"

DEFAULT_DPI = 300
PRINTER_DPI = 1200

A4_WIDTH_CM = 29.7
A4_HEIGHT_CM = 21

A4_WIDTH_BLEED_AREA_CM = 0.4
A4_PIXEL_WIDTH_BLEED_AREA = int(DEFAULT_DPI * A4_WIDTH_BLEED_AREA_CM / 2.54)

# For an A4 page, the size in pixels at 300dpi (without bleed area is (3508, 2480)
A4_PIXEL_WIDTH_DEFAULT_DPI = (
    int(DEFAULT_DPI * A4_WIDTH_CM / 2.54) - A4_PIXEL_WIDTH_BLEED_AREA * 2
)
A4_PIXEL_HEIGHT_DEFAULT_DPI = (
    int(DEFAULT_DPI * A4_HEIGHT_CM / 2.54) - A4_PIXEL_WIDTH_BLEED_AREA * 2
)


OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "mil": cv2.TrackerMIL_create,
}


def prRed(skk):
    print("\033[91m{}\033[00m".format(skk))


def prGreen(skk):
    print("\033[92m{}\033[00m".format(skk))
