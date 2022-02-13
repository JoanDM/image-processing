import argparse
from pathlib import Path

import file_manager.file_manager as file_manager
import video_editor

if __name__ == "__main__":

    parser = argparse.ArgumentParser("Extract frames from a video")
    parser.add_argument("-vid", nargs="?", help="Path to video", type=Path)
    parser.add_argument(
        "-tdir", nargs="?", help="Target dir to store frames", type=Path, default=None
    )

    args = parser.parse_args()
    path_to_video = args.vid
    target_dir = args.tdir

    if target_dir is None:
        target_dir = Path(f"{path_to_video.parents[0]}_frames")
        file_manager.create_directory(target_dir)

    video_editor.extract_frames_from_video(
        path_to_video=path_to_video,
        target_directory=target_dir
        # frame_prefix="test"
    )
