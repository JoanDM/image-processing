import argparse
from pathlib import Path

import cv2

import file_manager.file_manager as file_manager
from config import OPENCV_OBJECT_TRACKERS
from data_processing.data_processsor_class import JsonDataProcessor


def navigate_frames_and_create_annotation(directory_path, tracker_type_str, target_dir):
    """Launch a window to navigate through the frames in a directory. Draw a bounding box around the subject
    of interest and run OpenCV algorithms to automatically store the coordinates of the box on every frame

    :param directory_path: Path to directory with frames
    :param tracker_type_str: OpenCV tracking algorithm to be used
    :param target_dir: Path to directory to store bounding box coordinates as .json
    """
    json_processor = JsonDataProcessor()

    list_of_filenames = sorted(directory_path.glob("*.png"))
    cv2.namedWindow("Frame viewer")
    cv2.moveWindow("Frame viewer", 0, 0)

    cv2.namedWindow("Draw Bounding Box")
    cv2.setWindowProperty("Draw Bounding Box", cv2.WND_PROP_TOPMOST, 1)

    frame = cv2.imread(str(list_of_filenames[0]))
    initBB = cv2.selectROI(
        "Draw Bounding Box", frame, fromCenter=False, showCrosshair=True
    )
    cv2.destroyWindow("Draw Bounding Box")

    print(f"Initial coordinates x,y,w,h are: {initBB}")
    (x, y, w, h) = [int(v) for v in initBB]

    print(
        "A window that displays frames should be visible. Please set focus on the "
        "window.\nBasic commands:\n"
        "\n\tTo start/stop looping through the frames automatically, press 's'."
        "\n\tTo navigate to the next frame, press 'n'."
        "\n\tTo navigate to the previous frame, press or 'p'."
        "\n\tTo reset the tracker bounding box, press 'r'."
        "\n\tTo show the current stored key frames, press 'i'."
        "\n\tTo delete a stored key frame, press 'd'"
        "\n\tTo save and quit, press 'q'."
    )

    i = 0
    navigate_frames_automatically = False
    cv2.setWindowProperty("Frame viewer", cv2.WND_PROP_TOPMOST, 1)
    try:
        while True:
            file_path = list_of_filenames[i]
            frame = cv2.imread(str(file_path))

            if frame is None:
                break

            cv2.imshow("Frame viewer", frame)

            if initBB is not None and i == 0:
                tracker = OPENCV_OBJECT_TRACKERS[tracker_type_str]()
                tracker.init(frame, initBB)

            if initBB is not None:
                # grab the new bounding box coordinates of the object
                (success, box) = tracker.update(frame)

                plot_frame = frame.copy()

                winit, hinit = frame.shape[:2]
                wresize, hresize = plot_frame.shape[:2]
                wfactor = winit / wresize
                hfactor = hinit / hresize

                # check to see if the tracking was a success
                if success:
                    (xn, yn, wn, hn) = [int(v) for v in box]
                    if xn < 0 or yn < 0 or wn < 0 or hn < 0:
                        pass
                    else:
                        x, y, w, h = (xn, yn, wn, hn)

                    pos = (int(x / wfactor), int(y / hfactor))
                    size = (
                        int(x / wfactor + w / wfactor),
                        int(y / hfactor + h / hfactor),
                    )
                    cv2.rectangle(plot_frame, pos, size, (0, 0, 255), 10)

                else:
                    print("Tracker failed")

                cv2.imshow("Frame viewer", plot_frame)
                tracked_obj_frame_crop = frame.copy()

                tracked_obj_frame_crop = tracked_obj_frame_crop[y : y + h, x : x + w]

                (win_x, win_y, win_w, win_h) = cv2.getWindowImageRect("Frame viewer")
                cv2.moveWindow("Tracked result ", 0, win_y + win_h)
                cv2.imshow("Tracked result", tracked_obj_frame_crop)

            if not navigate_frames_automatically:
                key = cv2.waitKey(0)
            else:
                key = cv2.waitKey(1)

            # if 's' key is selected, start/stop automated loop through frames
            if key == ord("s"):
                navigate_frames_automatically = not navigate_frames_automatically

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

            # if 'r' key is pressed, reset tracker bounding box
            elif key == ord("r"):
                cv2.setWindowProperty("Draw Bounding Box", cv2.WND_PROP_TOPMOST, 1)
                initBB = cv2.selectROI(
                    "Draw Bounding Box", frame, fromCenter=False, showCrosshair=True
                )

                print(f"Initial coordinates x,y,w,h are: {initBB}")
                (x, y, w, h) = [int(v) for v in initBB]

                cv2.destroyWindow("Draw Bounding Box")

                tracker = OPENCV_OBJECT_TRACKERS[tracker_type_str]()
                tracker.init(frame, initBB)
                cv2.setWindowProperty("Frame viewer", cv2.WND_PROP_TOPMOST, 1)

            # if 'q' key is selected, quit
            elif key == ord("q"):
                cv2.destroyAllWindows()
                break

            # if no key is selected (timeout passed), loop automatically to next frame
            else:
                i += 1
                if i > len(list_of_filenames) - 1:
                    i = len(list_of_filenames) - 1

            json_processor.json_dict = {}
            json_processor.insert_key_val_to_current_json_dict(
                "filename", f"{file_path.name}"
            )
            json_processor.insert_key_val_to_current_json_dict(
                "bounding_box", [xn, yn, xn + wn, yn + hn]
            )
            json_processor.save_current_dict_to_json_file(
                target_filename=file_path.stem,
                target_directory=target_dir,
                print_output_file_path=False,
            )

    except KeyboardInterrupt:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Track a feature and store the bounding box as JSON"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing sequence of frames", type=Path
    )

    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store composition",
        type=Path,
        default=None,
    )

    args = parser.parse_args()
    target_dir = args.tdir

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_frame_annotations"
        file_manager.create_directory(target_dir)

    navigate_frames_and_create_annotation(
        directory_path=args.dir, tracker_type_str="csrt", target_dir=target_dir
    )
