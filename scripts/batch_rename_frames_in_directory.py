from pathlib import Path

import tqdm

from config import _results_dir_pathlib
from image_editor_class import ImageEditor


def batch_rename_frames_in_directory(path_to_directory, target_directory):
    editor = ImageEditor(target_directory)
    list_of_files = sorted(path_to_directory.glob("*.png"))

    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        editor.set_current_img(path_to_image=file_path)
        editor.save_current_img(target_file_name=f"{str(i).zfill(8)}")


if __name__ == "__main__":
    path_to_dir_with_frames = Path("path_to_dir_with_frames")

    target_dir = _results_dir_pathlib / "user_defined_directory_to_store_frames"

    batch_rename_frames_in_directory(path_to_dir_with_frames, target_dir)
