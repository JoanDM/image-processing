from pathlib import Path

import tqdm

from config import _results_dir_pathlib
from image_editor_class import ImageEditor


def batch_create_side_by_side_frame_composition_from_dir(
    target_directory,
    path_to_frames_in_comp_left_side,
    path_to_frames_in_comp_right_side,
):

    editor = ImageEditor(target_directory)
    list_of_left_comp_files = sorted(path_to_frames_in_comp_left_side.glob("*.png"))
    list_of_right_comp_files = sorted(path_to_frames_in_comp_right_side.glob("*.png"))

    left_comp_len = len(list_of_left_comp_files)
    right_comp_len = len(list_of_right_comp_files)
    if left_comp_len == right_comp_len:
        pass
    elif left_comp_len > right_comp_len:
        last_right_comp_file = list_of_right_comp_files[-1]
        for _ in range(left_comp_len - right_comp_len):
            list_of_right_comp_files.append(last_right_comp_file)

    elif right_comp_len > left_comp_len:
        last_left_comp_file = list_of_left_comp_files[-1]
        for _ in range(right_comp_len - left_comp_len):
            list_of_right_comp_files.append(last_left_comp_file)

    number_of_files = len(list_of_left_comp_files)

    for i, left_image_path, right_image_path in tqdm.tqdm(
        zip(range(number_of_files), list_of_left_comp_files, list_of_right_comp_files),
        total=number_of_files,
    ):

        editor.create_and_set_blank_image_as_current()

        editor.create_side_by_side_image_composition(left_image_path, right_image_path)

        editor.save_current_img(target_file_name=f"{str(i).zfill(8)}")


if __name__ == "__main__":
    path_to_frames_in_comp_left_side = Path("path_to_frames_in_comp_left_side")
    path_to_frames_in_comp_right_side = Path("path_to_frames_in_comp_right_side")

    target_directory = _results_dir_pathlib / "user_defined_target_dir"

    batch_create_side_by_side_frame_composition_from_dir(
        target_directory,
        path_to_frames_in_comp_left_side,
        path_to_frames_in_comp_right_side,
    )
