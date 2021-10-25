from pathlib import Path

from config import _results_dir_pathlib
from video_editor_class import VideoEditor

if __name__ == "__main__":
    path_to_video = Path("path_to_video")

    target_dir = _results_dir_pathlib / "user_defined_directory_to_store_frames"

    video_editor = VideoEditor(target_directory=target_dir)

    video_editor.extract_frames_from_video(
        path_to_video=path_to_video,
        # frame_prefix="test"
    )
