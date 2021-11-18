from pathlib import Path

import tqdm

from image_editor_class import ImageEditor


def insert_timestamps_on_frame_sequence_in_dir(
    path_to_directory, target_directory, dict_with_frame_id_and_message, fps=None
):
    if fps is None:
        fps = 30.0

    editor = ImageEditor(target_directory)
    list_of_files = sorted(path_to_directory.glob("*.png"))

    j = 0
    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        try:
            frame_main_title = dict_with_frame_id_and_message[i]
            j = 0
        except KeyError:
            pass

        editor.set_current_img(path_to_image=file_path)

        editor.insert_text_to_current_img(
            text=f"{frame_main_title}...\nFrame #{j + 1}\n{round(j * (1 / fps), 3):.3f} seconds\nTotal:{round(j * (1 / fps), 3):.3f} seconds",
            font_size=10,
            use_black_background=True,
        )

        editor.save_current_img(target_file_name=f"{str(i).zfill(8)}")

        j += 1


if __name__ == "__main__":

    dict_with_frame_id_and_message = {
        0: "Title used from frame id 0 until next dict item",
        # 23: "Title used from frame id 23 until next dict item"
    }

    dir_path = Path("path_to_dir_with_frames")

    target_dir = dir_path.parents[0] / f"{dir_path.stem}_extracted_frames"
    # target_dir = Path("user_defined_path")

    insert_timestamps_on_frame_sequence_in_dir(
        dir_path, target_dir, dict_with_frame_id_and_message
    )
