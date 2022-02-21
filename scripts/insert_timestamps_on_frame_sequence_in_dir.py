import argparse
import re
from pathlib import Path

import tqdm

import file_manager.file_manager as file_manager
import image_editor
from config import prRed


def insert_timestamps_on_frame_sequence_in_dir(
    list_of_files, target_directory, json_keyframes_file, fps
):
    # json_keyframes = JsonDataProcessor.load_json_file_content(json_keyframes_file)
    json_keyframes = file_manager.load_json_file_content(json_keyframes_file)

    time_measurements_tracker = dict.fromkeys(set(json_keyframes.values()), 0.0)

    j = 0
    for i, file_path in tqdm.tqdm(enumerate(list_of_files), total=len(list_of_files)):
        try:
            frame_main_title = json_keyframes[str(i)]
            j = 0
        except KeyError:
            time_measurements_tracker[frame_main_title] += 1.0 / fps

        img = image_editor.open_image(file_path)

        time_tracker_str = ""
        for value in sorted(set(json_keyframes.values())):
            try:
                time_tracker_str += f"\nTotal {value}: {round(time_measurements_tracker[value], 3):.3f} seconds"
            except KeyError:
                time_tracker_str += f"\nTotal {value}: {round(0.0, 3):.3f} seconds"

        img_w, img_h = img.size
        image_editor.insert_text_box(
            img=img,
            text=f"{frame_main_title}...\n"
            f"Frame #{j + 1} -- {round(j * (1 / fps), 3):.3f} seconds"
            f"{time_tracker_str}"
            f"\nTotal # frames: {i + 1} -- {round(i * (1 / fps), 3):.3f} seconds",
            box_width=img_w * 0.2,
            box_height=img_h * 0.15,
            position=(0, 0),
        )

        image_editor.insert_subtitle(
            img=img,
            text=frame_main_title,
        )
        image_editor.save_img(
            img=img,
            target_file_name=f"{str(i).zfill(8)}",
            target_directory=target_directory,
        )

        j += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Insert timestamps on a sequence of frames in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing images", type=Path
    )
    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store new frames",
        type=Path,
        default=None,
    )

    parser.add_argument(
        "-json",
        nargs="?",
        help="Path to JSON files conataining"
        "keyframes. You can create them with"
        "`scripts/create_keyframes_from_images_in_dir.py",
        type=Path,
        default=None,
    )

    args = parser.parse_args()
    target_dir = args.tdir

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_edited_frames"
        file_manager.create_directory(target_dir)

    list_of_files = file_manager.list_all_pngs_in_dir(args.dir)

    try:
        fps = int(re.findall("_(\d+)FPS", str(args.dir))[0])
    except IndexError:
        fps = int(
            input(
                prRed(
                    "Warning, original frame rate was not found in filename"
                    "Knowing the correct frame rate is critical for proper"
                    "time measurements. Enter the target FPS below\n>"
                )
            )
        )

    insert_timestamps_on_frame_sequence_in_dir(
        list_of_files=list_of_files,
        target_directory=target_dir,
        json_keyframes_file=args.json,
        fps=fps,
    )
