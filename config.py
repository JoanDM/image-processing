import os
from pathlib import Path

_base_dir = os.path.abspath(os.path.dirname(__file__))
_base_dir_pathlib = Path(_base_dir)
_results_dir_pathlib = Path(_base_dir) / "results"
_resources_dir_pathlib = Path(_base_dir) / "resources"
_tmp_dir_pathlib = _results_dir_pathlib / "tmp"

PRINTER_DPI = 1200
# For an A4 page, the size in pixels at 300dpi (without bleed area is (3508, 2480)
A4_PIXEL_WIDTH_300DPI = 3508
A4_PIXEL_HEIGH_300DPI = 2480


def prRed(skk):
    print("\033[91m{}\033[00m".format(skk))


def prGreen(skk):
    print("\033[92m{}\033[00m".format(skk))
