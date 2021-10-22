from pathlib import Path

import cv2
import tqdm

from config import prGreen


class VideoEditor(object):
    def __init__(self, target_directory):
        self.set_target_directory(target_directory)
        self.current_video = None
        self.current_video_path = None

    def set_target_directory(self, target_directory):
        self.target_directory = Path(str(target_directory))
        target_directory.mkdir(parents=True, exist_ok=True)

    def create_video_from_frames_in_dir(
        self, path_to_directory, target_video_name, fps
    ):

        list_of_files = sorted(path_to_directory.glob("*.png"))

        img_array = []

        print("\nFetching images...")
        for _, file_path in tqdm.tqdm(
            enumerate(list_of_files), total=len(list_of_files)
        ):
            img = cv2.imread(str(file_path))
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)

        target_video_path = self.target_directory / f"{target_video_name}.mp4"
        out = cv2.VideoWriter(
            str(target_video_path), cv2.VideoWriter_fourcc(*"MP4V"), fps, size
        )

        print("\nConstructing video...")
        for i in tqdm.tqdm(range(len(img_array))):
            out.write(img_array[i])
        out.release()
        prGreen(f"\n Done, video stored in {target_video_path}")
