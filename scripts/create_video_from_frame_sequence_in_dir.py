import argparse
from pathlib import Path

from config import _results_dir_pathlib
from video_editor_class import VideoEditor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Convert a sequence of frames in a directory to a video"
    )
    parser.add_argument(
        "dir", nargs="?", help="directory containing sequence of frames"
    )
    args = parser.parse_args()

    directory = args.dir

    if directory is not None:
        path_to_dir = Path(directory)
        target_dir = _results_dir_pathlib / "user_defined_directory_to_store_video"
        video_name = path_to_dir.stem
        frame_rate = 15

    else:
        path_to_dir = Path("path_to_directory_with_sequence_of_frames")
        target_dir = _results_dir_pathlib / "user_defined_directory_to_store_video"
        video_name = "user_defined_video_name_without_extension"
        frame_rate = 15

    video_editor = VideoEditor(target_directory=target_dir)

    video_editor.create_video_from_frames_in_dir(
        path_to_directory=path_to_dir,
        target_video_name=video_name,
        fps=frame_rate,
        freeze_final_frame=True,
        seconds_freezing_frame=1,
    )
