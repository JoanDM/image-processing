from pathlib import Path
import argparse
from config import DEFAULT_FRAME_RATE
import file_manager
import video_editor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create an image composition by stitching images in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing images", type=Path
    )
    parser.add_argument("-tdir", nargs="?", help="Target dir to store composition",
                        type=Path, default=None)

    parser.add_argument("-fname", nargs="?", help="name for the composition", type=str)
    parser.add_argument("-fps", nargs="?", help="target video frame rate", default=DEFAULT_FRAME_RATE, type=int)

    args = parser.parse_args()
    target_dir = args.tdir
    frame_rate = args.fps
    file_name = args.fname

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_stitched_videos"
        file_manager.create_directory(target_dir)

    if file_name is None:
        file_name = args.dir.stem

    list_of_paths_to_videos = file_manager.list_all_video_filepaths_in_dir(args.dir)

    video_editor.stitch_list_of_videos_side_by_side(
        list_of_paths_to_videos=list_of_paths_to_videos,
        fps=frame_rate,
        target_filename=file_name,
        target_directory=target_dir
    )
