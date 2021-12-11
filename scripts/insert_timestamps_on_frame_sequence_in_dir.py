import argparse
from pathlib import Path

import tqdm

from image_editor_class import ImageEditor


def insert_timestamps_on_frame_sequence_in_dir(
    path_to_directory,
    target_directory,
    dict_with_frame_id_and_message,
    font_size=20,
    fps=None,
):
    if fps is None:
        fps = 30.0

    editor = ImageEditor(target_directory)
    list_of_files = sorted(path_to_directory.glob("*.png"))

    time_measurements_tracker = dict.fromkeys(
        set(dict_with_frame_id_and_message.values()), 0.0
    )

    j = 0
    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        try:
            frame_main_title = dict_with_frame_id_and_message[i]
            j = 0
        except KeyError:
            time_measurements_tracker[frame_main_title] += 1.0 / fps

        editor.set_current_img(path_to_image=file_path)

        time_tracker_str = ""
        for value in sorted(set(dict_with_frame_id_and_message.values())):
            try:
                time_tracker_str += f"\nTotal {value}: {round(time_measurements_tracker[value],3):.3f} seconds"
            except KeyError:
                time_tracker_str += f"\nTotal {value}: {round(0.0, 3):.3f} seconds"

        editor.insert_text_to_current_img(
            text=f"{frame_main_title}...\n"
            f"Frame #{j + 1} -- {round(j * (1 / fps), 3):.3f} seconds"
            f"{time_tracker_str}"
            # f"\nTotal {frame_main_title}:{round(time_measurements_tracker[frame_main_title], 3):.3f} seconds,"
            f"\nTotal # frames: {i + 1} -- {round(i * (1 / fps), 3):.3f} seconds",
            max_font_size=font_size,
            use_black_background=True,
        )

        editor.save_current_img(target_file_name=f"{str(i).zfill(8)}")

        j += 1


if __name__ == "__main__":

    dict_with_frame_id_and_message = {
        0: "Title used from frame id 0 until next dict item",
        # 23: "Title used from frame id 23 until next dict item"
    }

    parser = argparse.ArgumentParser("Extract frames from a video")
    parser.add_argument("dir", nargs="?", help="path to directory with frames")
    parser.add_argument("tdir", nargs="?", help="target dir to store video")
    args = parser.parse_args()

    dir_path = args.dir
    target_dir = args.tdir

    if dir_path is not None:
        dir_path = Path(dir_path)
        if target_dir is not None:
            target_dir = Path(target_dir)
        else:
            target_dir = dir_path.parents[0] / f"{dir_path.stem}_edited_frames"

    else:
        dir_path = Path("path_to_dir_with_frames")
        target_dir = dir_path.parents[0] / f"{dir_path.stem}_edited_frames"
    # target_dir = Path("user_defined_path")

    font_size = 30

    insert_timestamps_on_frame_sequence_in_dir(
        dir_path, target_dir, dict_with_frame_id_and_message, font_size
    )
