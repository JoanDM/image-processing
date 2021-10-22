from pathlib import Path

import tqdm

from config import _results_dir_pathlib, _tmp_dir_pathlib
from image_editor_class import ImageEditor
from video_editor_class import VideoEditor


def edit_frame_sequence_and_create_video(path_to_directory_with_frames, video_name):
    target_directory_for_frames = _tmp_dir_pathlib
    target_directory_for_video = _results_dir_pathlib / "video"

    image_editor = ImageEditor(target_directory_for_frames)
    video_editor = VideoEditor(target_directory_for_video)

    list_of_files = sorted(path_to_directory_with_frames.glob("*.png"))

    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        image_editor.set_current_img(path_to_image=file_path)
        image_editor.insert_rectangle_to_image(
            x_coord=0,
            y_coord=0,
            rectangle_height=300,
            rectangle_width=700,
        )

        image_editor.insert_text_to_image(
            text=f"Frame #{i + 1}\n{round(i * 0.0333333, 3)} seconds"
        )
        image_editor.resize_image((1280, 720))
        image_editor.save_current_img(target_file_name=f"{str(i).zfill(3)}")

    video_editor.create_video_from_frames_in_dir(
        path_to_directory=target_directory_for_frames,
        target_video_name=video_name,
        fps=0.5,
    )

    image_editor.cleanup_tmp_dir()


if __name__ == "__main__":
    dir_path = Path("path_to_directory_with_frames")

    target_video_name = "user_defined_video_name"

    edit_frame_sequence_and_create_video(dir_path, target_video_name)
