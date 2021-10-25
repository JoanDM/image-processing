from pathlib import Path

from config import _results_dir_pathlib
from video_editor_class import VideoEditor

if __name__ == "__main__":
    path_to_dir = Path("path_to_directory_with_sequence_of_frames")
    target_dir = _results_dir_pathlib / "user_defined_directory_to_store_video"
    video_name = "user_defined_video_name_without_extension"
    frame_rate = 2

    video_editor = VideoEditor(target_directory=target_dir)

    video_editor.create_video_from_frames_in_dir(
        path_to_directory=path_to_dir, target_video_name=video_name, fps=frame_rate
    )
