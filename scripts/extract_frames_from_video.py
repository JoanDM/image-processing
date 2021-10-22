from pathlib import Path

from config import _results_dir_pathlib
from image_editor_class import ImageEditor

if __name__ == "__main__":
    path_to_video = Path("path_to_video")

    target_dir = _results_dir_pathlib / "user_defined_directory_to_store_frames"

    image_editor = ImageEditor(target_directory=target_dir)

    image_editor.extract_frames_from_video(
        path_to_video=path_to_video,
        # frame_prefix="test"
    )
