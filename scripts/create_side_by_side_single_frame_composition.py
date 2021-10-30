from pathlib import Path

from config import _results_dir_pathlib
from image_editor_class import ImageEditor


def create_side_by_side_frame_composition(
    target_directory,
    path_to_left_side_image,
    path_to_right_side_image,
):
    editor = ImageEditor(target_directory)

    editor.create_and_set_blank_image_as_current()

    editor.create_side_by_side_image_composition(
        path_to_left_side_image, path_to_right_side_image
    )

    editor.save_current_img("test")


if __name__ == "__main__":
    path_to_left_side_image = Path("path_to_left_image_in_split_comp")
    path_to_right_side_image = Path("path_to_right_image_in_split_comp")

    target_directory = _results_dir_pathlib / "test_comp"

    create_side_by_side_frame_composition(
        target_directory, path_to_left_side_image, path_to_right_side_image
    )
