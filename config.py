import os
from pathlib import Path

_base_dir = os.path.abspath(os.path.dirname(__file__))
_base_dir_pathlib = Path(_base_dir)
_results_dir_pathlib = Path(_base_dir) / "results"
_resources_dir_pathlib = Path(_base_dir) / "resources"
_tmp_dir_pathlib = _results_dir_pathlib / "tmp"


def prRed(skk):
    print("\033[91m{}\033[00m".format(skk))


def prGreen(skk):
    print("\033[92m{}\033[00m".format(skk))
