import argparse
from pathlib import Path

import cv2

from config import _results_dir_pathlib, prGreen
from data_processing.data_processsor_class import JsonDataProcessor


def define_key_frame(frame_index, dict_with_keyframes):
    keyframe_name = input(
        f"\nSet a name for the keyframe starting from "
        f"frame #{frame_index}\nPreviously defined keyframes:"
        f"\n{dict_with_keyframes}\nIn case the keyframe is "
        f"already in the list, you can simply type the "
        f"corresponding integer."
        f"\nPress Enter if you don't want to define a "
        f"keyframe\n>"
    )
    if keyframe_name.isdigit():
        dict_with_keyframes[frame_index] = dict_with_keyframes[int(keyframe_name)]

    elif keyframe_name == "":
        pass
    else:
        dict_with_keyframes[frame_index] = keyframe_name
    return dict_with_keyframes


def navigate_frames_and_create_keyframes(directory_path):
    dict_with_keyframes = {}
    i = 0
    cv2.namedWindow("Frame viewer frame")
    cv2.moveWindow("Frame viewer", 0, 0)

    list_of_filenames = sorted(directory_path.glob("*.png"))

    cv2.imshow("Frame viewer", cv2.imread(str(list_of_filenames[0])))
    dict_with_keyframes = define_key_frame(0, dict_with_keyframes)

    print(
        "A window that displays frames should be visible. Please set focus on the "
        "window.\n\nBasic commands:\n"
        "\n\tTo navigate to the next"
        "frame, press or hold 'n'.\n\tTo navigate to the previous frame, press or 'p'."
        "\n\tTo set a keyframe in the active frame, press 's'."
        "\n\tTo show the current stored key frames, press 'i'.\n\tTo delete a stored "
        "key frame, press 'd'\n\tTo quit, press 'q'."
    )

    i += 1
    try:
        while True:
            frame = cv2.imread(str(list_of_filenames[i]))

            if frame is None:
                return 0

            cv2.imshow("Frame viewer", frame)

            key = cv2.waitKey(0)

            # if's' key is selected, we are going to define a new keyframe
            if key == ord("s"):
                dict_with_keyframes = define_key_frame(i, dict_with_keyframes)

            # if'n' key is selected, jump to the next keyframe
            elif key == ord("n"):
                i += 1
                if i > len(list_of_filenames) - 1:
                    i = len(list_of_filenames) - 1

            # if'n' key is selected, jump to the previous keyframe
            elif key == ord("p"):
                i -= 1
                if i < 0:
                    i = 0

            # if'i' key is selected, show stored keyframes
            elif key == ord("i"):
                print(f"Active frame #{i}\nStored keyframes: {dict_with_keyframes}")

            # if 'i' key is selected, let user delete keyframe
            elif key == ord("d"):
                print(f"Stored keyframes: {dict_with_keyframes}")
                keyframe_key_to_del = input(
                    "Insert key of the keyframe to be deleted\n>"
                )
                if keyframe_key_to_del.isdigit():
                    del dict_with_keyframes[int(keyframe_key_to_del)]

            # if 'q' key is selected, quit
            elif key == ord("q"):
                cv2.destroyAllWindows()
                break

    except KeyboardInterrupt:
        cv2.destroyAllWindows()

    return dict_with_keyframes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Convert a sequence of frames in a directory to a video"
    )
    parser.add_argument(
        "dir", nargs="?", help="directory containing sequence of frames"
    )
    parser.add_argument("tdir", nargs="?", help="target dir to store video")
    args = parser.parse_args()

    directory = args.dir

    target_dir = args.tdir

    if directory is not None:
        path_to_dir = Path(directory)

    else:
        path_to_dir = Path("path_to_directory_with_sequence_of_frames")

    if target_dir is not None:
        target_dir = Path(directory)
    else:
        target_dir = _results_dir_pathlib / f"{path_to_dir.stem}_stored_keyframes"

    dict_with_keyframes = navigate_frames_and_create_keyframes(path_to_dir)

    data_processor = JsonDataProcessor(target_dir)
    data_processor.set_current_json_dict(dict_with_keyframes)
    data_processor.save_current_dict_to_json_file(
        target_filename=f"{path_to_dir.stem}_keyframes"
    )
    prGreen(f"Success! The following key frames were stored:")
    data_processor.print_current_json_dict_content()
