from pathlib import Path

import tqdm

from config import _results_dir_pathlib
from image_editor_class import ImageEditor


def insert_frame_info_on_image_sequence_in_dir(
    path_to_directory, target_directory=None
):
    editor = ImageEditor(target_directory)
    list_of_files = sorted(path_to_directory.glob("*.png"))

    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        editor.set_current_img(path_to_image=file_path)
        editor.insert_rectangle_to_image(
            x_coord=0,
            y_coord=0,
            rectangle_height=300,
            rectangle_width=700,
        )

        editor.insert_text_to_image(
            text=f"Frame #{i+1}\n{round(i*0.0333333,3)} seconds"
        )

        editor.save_current_img(target_file_name=f"{str(i).zfill(3)}")


if __name__ == "__main__":
    dir_path = Path("path_to_directory_with_images")

    target_directory = _results_dir_pathlib / "user_defined_directory_to_store_frames"

    insert_frame_info_on_image_sequence_in_dir(dir_path, target_directory)
