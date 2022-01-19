from pathlib import Path

from config import _results_dir_pathlib
from image_editor_class import ImageEditor


def stitch_list_of_images_side_by_side(
    target_directory,
    path_to_dir_with_images,
):
    editor = ImageEditor(target_directory)

    editor.create_and_set_blank_image_as_current()

    list_of_paths_to_images = sorted(path_to_dir_with_images.glob("*.png"))

    editor.stitch_images_side_by_side(list_of_paths_to_images)

    editor.save_current_img("test")


if __name__ == "__main__":
    path_to_dir_with_images = Path("path_to_dir_with_images_sorted")

    target_directory = _results_dir_pathlib / "stitched_images"

    stitch_list_of_images_side_by_side(target_directory, path_to_dir_with_images)
