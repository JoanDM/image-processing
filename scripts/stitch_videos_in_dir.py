import argparse
from pathlib import Path

import file_manager.file_manager as file_manager
import video_editor
from config import DEFAULT_FRAME_RATE

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create a video composition by stitching videos in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing videos", type=Path
    )
    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store video composition",
        type=Path,
        default=None,
    )

    parser.add_argument("-fname", nargs="?", help="name for the composition", type=str)
    parser.add_argument(
        "-fps",
        nargs="?",
        help="target video frame rate",
        default=DEFAULT_FRAME_RATE,
        type=int,
    )
    parser.add_argument("-nosubs", help="insert video subtitles", action="store_true")

    args = parser.parse_args()
    target_dir = args.tdir
    frame_rate = args.fps
    file_name = args.fname

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_stitched_videos"
        file_manager.create_directory(target_dir)

    if file_name is None:
        file_name = args.dir.stem

    if args.nosubs:
        list_of_subtitles = None
    else:
        list_of_subtitles = file_manager.list_all_video_filenams_in_dir(args.dir)

    list_of_paths_to_videos = file_manager.list_all_video_filepaths_in_dir(args.dir)

    video_editor.stitch_list_of_videos_side_by_side(
        list_of_paths_to_videos=list_of_paths_to_videos,
        fps=frame_rate,
        target_filename=file_name,
        target_directory=target_dir,
        list_of_subtitles=list_of_subtitles,
    )
