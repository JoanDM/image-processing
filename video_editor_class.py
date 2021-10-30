from pathlib import Path

import cv2
import tqdm

from config import _tmp_dir_pathlib, prGreen, prRed


class VideoEditor(object):
    def __init__(self, target_directory):
        self.set_target_directory(target_directory)

    def set_target_directory(self, target_directory):
        self.target_directory = Path(str(target_directory))
        target_directory.mkdir(parents=True, exist_ok=True)

    def create_video_from_frames_in_dir(
        self,
        path_to_directory,
        target_video_name,
        fps,
        freeze_final_frame=False,
        seconds_freezing_frame=2,
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

        if freeze_final_frame:
            for _ in range(seconds_freezing_frame * fps):
                img_array.append(img)

        target_video_path = self.target_directory / f"{target_video_name}.mp4"
        out = cv2.VideoWriter(
            str(target_video_path),
            cv2.VideoWriter_fourcc(*"avc1"),
            fps,
            size,
            isColor=True,
        )

        print("\nConstructing video...")
        for i in tqdm.tqdm(range(len(img_array))):
            out.write(img_array[i])
        out.release()

        prGreen(f"\n Done, video stored in {target_video_path}")

    def extract_frames_from_video(self, path_to_video, frame_prefix=""):

        vidcap = cv2.VideoCapture(str(path_to_video))

        fps = vidcap.get(cv2.CAP_PROP_FPS)

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
            f"\nExtracting {total_number_of_frames} frames from {path_to_video} to {self.target_directory}..."
        )
        print(f"Video frame rate is {fps}")
        for _ in tqdm.tqdm(range(total_number_of_frames)):
            file_name = (
                self.target_directory
                / f"{f'{frame_prefix}_' if frame_prefix else ''}{str(count).zfill(8)}.png"
            )
            success, image = vidcap.read()
            cv2.imwrite(str(file_name), image)
            count += 1

        return fps

    def cleanup_tmp_dir(self):
        try:
            [f.unlink() for f in _tmp_dir_pathlib.glob("*") if f.is_file()]
        except PermissionError:
            prRed(
                f"Error when cleaning up {_tmp_dir_pathlib} "
                f"Check Full Disk Access settings on Mac"
            )
