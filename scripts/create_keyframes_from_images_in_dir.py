import argparse
from pathlib import Path

import cv2

import file_manager.file_manager as file_manager
from config import pr_green
from data_processing.data_processsor_class import JsonDataProcessor


def navigate_frames_and_create_keyframes(directory_path, target_dir):
    """Launch a window to navigate through the frames in a directory. Give a name to every fraction of the sequence with a dict of keyframes

    :param directory_path: Path to directory with frames
    :param target_dir: Path to directory to store keyframe names as .json
    """
    json_processor = JsonDataProcessor()
    json_processor.json_dict = {}
    i = 0
    cv2.namedWindow("Frame viewer frame")
    cv2.moveWindow("Frame viewer", 0, 0)

    list_of_filenames = sorted(directory_path.glob("*.png"))

    cv2.imshow("Frame viewer", cv2.imread(str(list_of_filenames[0])))
    define_key_frame(json_processor, i)

    print(
        "A window that displays frames should be visible. Please set focus on the "
        "window.\nBasic commands:\n"
        "\n\tTo start/stop looping through the frames automatically, press 's'."
        "\n\tTo navigate to the next frame, press 'n'."
        "\n\tTo navigate to the previous frame, press or 'p'."
        "\n\tTo insert a new key frame, press 'i'."
        "\n\tTo show the currently stored key frames, press 'r'."
        "\n\tTo delete a stored key frame, press 'd'"
        "\n\tTo save and quit, press 'q'."
    )

    i += 1
    navigate_frames_automatically = False
    try:
        while True:
            file_path = list_of_filenames[i]
            frame = cv2.imread(str(file_path))

            if frame is None:
                break

            cv2.imshow("Frame viewer", frame)

            if not navigate_frames_automatically:
                key = cv2.waitKey(0)
            else:
                key = cv2.waitKey(1)

            # if 's' key is selected, start/stop automated loop through frames
            if key == ord("s"):
                navigate_frames_automatically = not navigate_frames_automatically

            # if 'i' key is selected, we are going to insert a new keyframe
            if key == ord("i"):
                define_key_frame(json_processor, i)

            # if 'n' key is selected, jump to the next keyframe
            elif key == ord("n"):
                i += 1
                if i > len(list_of_filenames) - 1:
                    i = len(list_of_filenames) - 1

            # if 'p' key is selected, jump to the previous keyframe
            elif key == ord("p"):
                i -= 1
                if i < 0:
                    i = 0

            # if 'r' key is selected, show stored keyframes
            elif key == ord("r"):
                print(f"Active frame #{i}\nStored keyframes:")
                json_processor.print_current_json_dict_content()

            # if 'd' key is selected, let user delete keyframe
            elif key == ord("d"):
                print(f"Stored keyframes:")
                json_processor.print_current_json_dict_content()
                keyframe_key_to_del = input(
                    "Insert key of the keyframe to be deleted\n>"
                )
                if keyframe_key_to_del.isdigit():
                    json_processor.delete_key_from_current_json_dict(
                        int(keyframe_key_to_del)
                    )

            # if 'q' key is selected, quit
            elif key == ord("q"):
                cv2.destroyAllWindows()
                break

            # if no key is selected (timeout passed), loop automatically to next frame
            else:
                i += 1
                if i > len(list_of_filenames) - 1:
                    i = len(list_of_filenames) - 1

        json_processor.save_current_dict_to_json_file(
            target_filename=f"{directory_path.stem}_keyframes",
            target_directory=target_dir,
            print_output_file_path=True,
        )
        pr_green(f"Success! The following key frames were stored:")
        json_processor.print_current_json_dict_content()

    except KeyboardInterrupt:
        cv2.destroyAllWindows()


def define_key_frame(json_dict, frame_index):
    """Create a new entry to a json dict for a specific key index.
    If the entry is a key already present in the dictionary, copy the corresponding entry.

    :param json_dict: Dict. key: int (frame index), val: str.
    :param index: _description_
    """
    keyframe_name = input(
        f"\nSet a name for the keyframe starting from "
        f"frame #{frame_index}\nPreviously defined keyframes:"
        f"\n{json_dict}\nIn case the keyframe is "
        f"already in the list, you can simply type the "
        f"corresponding integer."
        f"\nPress Enter if you don't want to define a "
        f"keyframe\n>"
    )
    if keyframe_name.isdigit():
        json_dict[frame_index] = json_dict[keyframe_name]
    elif keyframe_name == "":
        pass
    else:
        json_dict[frame_index] = keyframe_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create a list of key frames (key=frame id, value=clip_name) and store it as JSON"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing sequence of frames", type=Path
    )

    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store keyframes",
        type=Path,
        default=None,
    )

    args = parser.parse_args()
    target_dir = args.tdir

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_stored_keyframes"
        file_manager.create_directory(target_dir)

    navigate_frames_and_create_keyframes(args.dir, target_dir)
