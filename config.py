import os
from pathlib import Path

import cv2

_base_dir = os.path.abspath(os.path.dirname(__file__))
_base_dir_pathlib = Path(_base_dir)
_results_dir_pathlib = _base_dir_pathlib / "results"
_resources_dir_pathlib = _base_dir_pathlib / "resources"
_tmp_dir_pathlib = _results_dir_pathlib / "tmp"
_ffmpeg_path = Path("/usr/local/bin/ffmpeg")
_ffprobe_path = Path("/usr/local/bin/ffprobe")
_default_font_path = Path("/System/Library/Fonts/SFNS.ttf")
_1_minute_timer_video_path = _resources_dir_pathlib / "1min_b&w_timer.mp4"

_default_frame_rate = 30
_default_subtitle_height_percentage = 0.05

_default_dpi = 300
_printer_dpi = 1200

_a4_width_cm = 29.7
_a4_height_cm = 21

_a4_width_bleed_area_cm = 0.4
_a4_pixel_width_bleed_area = int(_default_dpi * _a4_width_bleed_area_cm / 2.54)

# For an A4 page, the size in pixels at 300dpi (without bleed area is (3508, 2480)
# _a4_pixel_width_default_dpi = (
#     int(_default_dpi * _a4_width_cm / 2.54) - _a4_pixel_width_bleed_area * 2
# )
# _a4_pixel_height_default_dpi = (
#     int(_default_dpi * _a4_height_cm / 2.54) - _a4_pixel_width_bleed_area * 2
# )


_opencv_object_trackers = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "mil": cv2.TrackerMIL_create,
}


def pr_red(skk):
    """Convenient method to print red text in the console
    :param skk: Text to output
    """
    print("\033[91m{}\033[00m".format(skk))


def pr_green(skk):
    """Convenient method to print green text in the console
    :param skk: Text to output
    """
    print("\033[92m{}\033[00m".format(skk))
