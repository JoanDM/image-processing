import argparse
from pathlib import Path

import cv2

from config import OPENCV_OBJECT_TRACKERS, _results_dir_pathlib


def navigate_frames_and_create_annotation(directory_path, tracker_type_str):

    list_of_filenames = sorted(directory_path.glob("*.png"))
    cv2.namedWindow("Frame viewer")
    cv2.moveWindow("Frame viewer", 0, 0)
    cv2.imshow("Frame viewer", cv2.imread(str(list_of_filenames[0])))

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
        "\n\tTo quit, press 'q'."
    )

    i = 0
    navigate_frames_automatically = False
    try:
        while True:
            frame = cv2.imread(str(list_of_filenames[i]))

            if frame is None:
                return 0

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

                cv2.imshow("Tracked result", tracked_obj_frame_crop)

            if not navigate_frames_automatically:
                print("waiting for key")
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

            # if 'n' key is selected, jump to the previous keyframe
            elif key == ord("p"):
                i -= 1
                if i < 0:
                    i = 0

            # if 'r' key is pressed, reset tracker bounding box
            elif key == ord("r"):
                initBB = cv2.selectROI(
                    "Draw Bounding Box", frame, fromCenter=False, showCrosshair=True
                )

                print(f"Initial coordinates x,y,w,h are: {initBB}")
                (x, y, w, h) = [int(v) for v in initBB]

                cv2.destroyWindow("Draw Bounding Box")

                tracker = OPENCV_OBJECT_TRACKERS[tracker_type_str]()
                tracker.init(frame, initBB)

            # if 'q' key is selected, quit
            elif key == ord("q"):
                cv2.destroyAllWindows()
                break

            # if no key is selected (timeout passed), loop automatically to next frame
            else:
                i += 1
                if i > len(list_of_filenames) - 1:
                    i = len(list_of_filenames) - 1

    except KeyboardInterrupt:
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create a list of key frames (key=frame id, value=clip_name) and store it as JSON"
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
        target_dir = _results_dir_pathlib / f"{path_to_dir.stem}_frame_annotations"

    _ = navigate_frames_and_create_annotation(
        directory_path=path_to_dir, tracker_type_str="csrt"
    )
