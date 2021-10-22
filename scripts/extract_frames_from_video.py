from pathlib import Path

import cv2
import tqdm

from config import _results_dir_pathlib


def extract_frames_from_video(path_to_video, target_directory, frame_prefix=""):
    target_directory.mkdir(parents=True, exist_ok=True)

    vidcap = cv2.VideoCapture(str(path_to_video))

    count = 0

    # Loop through the video to get the number of frames
    total_number_of_frames = 0
    while vidcap.isOpened():
        frame_exists, frame = vidcap.read()
        if frame_exists:
            total_number_of_frames += 1
        else:
            break

    vidcap = cv2.VideoCapture(str(path_to_video))

    print(
        f"\nExtracting {total_number_of_frames} frames from {path_to_video} to {target_directory}..."
    )
    for _ in tqdm.tqdm(range(total_number_of_frames)):
        file_name = (
            target_directory
            / f"{f'{frame_prefix}_' if frame_prefix else ''}{str(count).zfill(4)}.png"
        )
        success, image = vidcap.read()
        cv2.imwrite(str(file_name), image)
        count += 1


if __name__ == "__main__":
    path_to_video = Path("path_to_video")

    target_dir = _results_dir_pathlib / "user_defined_directory_to_store_frames"

    extract_frames_from_video(path_to_video, target_dir)
