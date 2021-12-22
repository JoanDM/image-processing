import argparse
from pathlib import Path

from config import _results_dir_pathlib, prGreen
from video_editor_class import VideoEditor

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Extract frames from a video")
    parser.add_argument("vid", nargs="?", help="path to video")
    parser.add_argument("tdir", nargs="?", help="target dir to store video")
    args = parser.parse_args()

    path_to_video = args.vid
    target_dir = args.tdir

    if path_to_video is not None:
        path_to_video = Path(path_to_video)
    else:
        path_to_video = Path("path_to_video")

    if target_dir is not None:
        target_dir = Path(target_dir)
    else:
        target_dir = _results_dir_pathlib / f"{path_to_video.stem}_extracted_frames"

    video_editor = VideoEditor(target_directory=target_dir)

    video_editor.extract_frames_from_video(
        path_to_video=path_to_video,
        # frame_prefix="test"
    )

    prGreen(f"Success! Extracted frames can be found at {target_dir}")
