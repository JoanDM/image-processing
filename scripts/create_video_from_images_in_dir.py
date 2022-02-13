import argparse
from pathlib import Path
from config import DEFAULT_FRAME_RATE, prGreen
import video_editor
import webbrowser

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create a video from a sequence of frames in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="directory containing sequence of frames", type=str
    )
    parser.add_argument("-tdir", nargs="?", help="target dir to store video", type=str, default=None)
    parser.add_argument("-vname", nargs="?", help="name for the video", type=str)
    parser.add_argument("-fps", nargs="?", help="target video frame rate", default=DEFAULT_FRAME_RATE, type=int)
    parser.add_argument("-freeze", nargs="?", help="freeze last frames for a second", default=True, type=bool)

    args = parser.parse_args()
    directory = Path(args.dir)
    target_dir = args.tdir
    frame_rate = args.fps
    video_name = args.vname
    freeze_bool = args.freeze

    if target_dir is None:
        target_dir = directory.parents[0] / f"{directory.stem}_video"

    if video_name is None:
        video_name = directory.stem

    video_editor.create_video_from_frames_in_dir(
        path_to_directory=directory,
        target_directory=target_dir,
        target_video_name=video_name,
        fps=frame_rate,
        freeze_last_frame=freeze_bool,
        seconds_freezing_frame=1,
        insert_subtitles=False
    )

    # prGreen(f"\n Done, video stored in {target_dir / video_name}")
    # new = 2  # open in a new tab, if possible
    # webbrowser.open(f"file://{target_dir/video_name}", new=new)