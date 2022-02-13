from pathlib import Path

import tqdm

from config import _results_dir_pathlib, _tmp_dir_pathlib
from image_editor_class import ImageEditor
from video_editor_class import VideoEditor


def extract_frames_and_insert_timestamps_from_video(path_to_video, target_directory):
    video_editor = VideoEditor(_tmp_dir_pathlib)

    video_fps = video_editor.extract_frames_from_video(path_to_video)

    print(f"\nEditing frames... Frames will be saved in {target_directory}")

    list_of_files = sorted(video_editor.target_directory.glob("*.png"))

    image_editor = ImageEditor(target_directory)

    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        image_editor.set_current_img(path_to_image=file_path)
        image_editor.insert_rectangle_to_current_img(
            x_coord=0,
            y_coord=0,
            rectangle_height=300,
            rectangle_width=700,
        )

        image_editor.insert_text_to_current_img(
            text=f"Frame #{i + 1}\n{round(i * (1/video_fps), 3)} seconds"
        )
        image_editor.resize_current_img((1280, 720))
        image_editor.save_current_img(target_file_name=f"{str(i).zfill(8)}")

    video_editor.cleanup_tmp_dir()


if __name__ == "__main__":

    dir_path_to_video = Path(f"path_to_video")

    target_directory = Path(_results_dir_pathlib / f"user_defined_target_directory")

    extract_frames_and_insert_timestamps_from_video(dir_path_to_video, target_directory)
