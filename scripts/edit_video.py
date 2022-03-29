import argparse
from pathlib import Path

import cv2
import tqdm

import file_manager.file_manager as file_manager
import image_editor
import video_editor
from config import _default_frame_rate


def edit_video(video_path, target_directory, target_filename):
    """Custom method to modify a video as you wish. Since the scope is very broad, you should edit the script and tailor it to your objectives.
    Some examples of the method capabilities:
        - Instert a subtitle to the video
        - Make a slow-mo version of the video

    :param video_path: Path to video file
    :param target_directory: Target directory to store modified video file
    :param target_filename: Target name for the modified video file, without suffix
    """

    # Insert any video operations here
    Video1 = video_editor.convert_video_frame_rate(
        path_to_video=video_path,
        target_fps=_default_frame_rate,
        target_directory=target_directory,
        target_file_name=f"{video_path.stem}_{_default_frame_rate}fps{video_path.suffix}",
    )
    cap1 = cv2.VideoCapture(str(Video1))
    target_frame_rate = 10
    subtitle = file_name

    # Save file
    target_file_path = file_manager.find_new_unique_file_path(
        target_file_path=target_directory / f"{target_filename}.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    videowriter = None
    num_frames_vid = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in tqdm.tqdm(range(num_frames_vid)):
        if i < num_frames_vid:
            _, frame1 = cap1.read()

        if i == (num_frames_vid):
            break

        img = image_editor.convert_opencv_format_to_pil(frame1)
        if subtitle:
            image_editor.insert_subtitle(img=img, text=subtitle)

        if videowriter is None:
            size = img.size
            videowriter = cv2.VideoWriter(
                str(target_file_path), fourcc, target_frame_rate, size
            )
        img = image_editor.convert_pil_to_opencv_format(img)

        videowriter.write(img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
    file_manager.move_file_to_trash(Video1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Manipulate a video")
    parser.add_argument("-vid", nargs="?", help="Path to video", type=Path)
    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store modified videos",
        type=Path,
        default=None,
    )
    parser.add_argument("-fname", nargs="?", help="name for the composition", type=str)

    args = parser.parse_args()
    target_dir = args.tdir
    file_name = args.fname

    if target_dir is None:
        target_dir = args.vid.parents[0] / f"{args.vid.stem}_edited"

    if file_name is None:
        file_name = args.vid.stem

    file_manager.create_directory(target_dir)

    edit_video(args.vid, target_dir, file_name)
