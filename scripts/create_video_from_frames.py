from pathlib import Path

import cv2
import tqdm

from config import _results_dir_pathlib


def create_video_from_frames_in_dir(
    path_to_directory, target_directory, video_name, fps
):
    target_directory.mkdir(parents=True, exist_ok=True)

    list_of_files = sorted(path_to_directory.glob("*.png"))

    img_array = []

    print("\nFetching images...")
    for file_path in tqdm.tqdm(list_of_files):
        img = cv2.imread(str(file_path))
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    target_video_path = target_directory / f"{video_name}.mp4"
    out = cv2.VideoWriter(
        str(target_video_path), cv2.VideoWriter_fourcc(*"DIVX"), fps, size
    )

    print("\nConstructing video...")
    for i in tqdm.tqdm(range(len(img_array))):
        out.write(img_array[i])
    out.release()


if __name__ == "__main__":
    path_to_dir = Path("path_to_directory_with_sequence_of_frames")
    target_dir = _results_dir_pathlib / "user_defined_directory_to_store_video"
    video_name = "user_defined_video_name_without_extension"
    frame_rate = 0.5

    create_video_from_frames_in_dir(path_to_dir, target_dir, video_name, frame_rate)
