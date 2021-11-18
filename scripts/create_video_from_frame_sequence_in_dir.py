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
    parser.add_argument("tdir", nargs="?", help="target dir to store video")
    args = parser.parse_args()

    directory = args.dir

    target_dir = args.tdir

    if directory is not None:
        path_to_dir = Path(directory)
        if target_dir is not None:
            target_dir = Path(target_dir)
        else:
            target_dir = path_to_dir.parents[0] / f"{path_to_dir.stem}_video"

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
        frames_to_freeze=[],
        freeze_last_frame=True,
        seconds_freezing_frame=2,
    )
