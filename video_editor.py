import cv2
import tqdm
import subprocess
import webbrowser
from config import _tmp_dir_pathlib, prGreen, prRed, DEFAULT_FRAME_RATE
import image_editor
import file_manager


def create_video_from_frames_in_dir(
        path_to_directory,
        target_directory,
        target_video_name,
        fps,
        frames_to_freeze=[],
        freeze_last_frame=False,
        seconds_freezing_frame=2,
        insert_subtitles=False
):
    file_manager.create_directory(target_directory)
    target_video_name = file_manager.find_new_unique_filename(target_directory / f"{target_video_name}.mp4")
    target_video_path = target_directory / f"{target_video_name}.mp4"
    list_of_files = file_manager.list_all_pngs_in_dir(path_to_directory)

    img = cv2.imread(str(list_of_files[0]))

    height, width, layers = img.shape
    size = (width, height)

    out = cv2.VideoWriter(
        str(target_video_path),
        cv2.VideoWriter_fourcc(*"avc1"),
        fps,
        size,
        isColor=True,
    )

    print("\nConstructing video...")
    for i, file_path in tqdm.tqdm(
            enumerate(list_of_files), total=len(list_of_files)
    ):
        img = image_editor.open_image(file_path)
        if insert_subtitles:
            image_editor.insert_subtitle(
                img=img,
                text=file_path.stem,
                color="white",
                subtitle_height_percentage=0.1
            )

        img = image_editor.convert_pil_to_opencv_format(img=img)

        out.write(img)

        if frames_to_freeze:
            if i in frames_to_freeze:
                for _ in range(seconds_freezing_frame * fps):
                    out.write(img)

    if freeze_last_frame:
        for _ in range(seconds_freezing_frame * fps):
            out.write(img)

    out.release()


def extract_frames_from_video(path_to_video, target_directory, frame_prefix=""):
    vidcap = cv2.VideoCapture(str(path_to_video))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    target_directory = target_directory.parents[0] / f"{target_directory.stem}_{fps}FPS"
    file_manager.create_directory(target_directory)

    count = 0

    # Loop through the video to get the number of frames
    total_number_of_frames = 0
    while vidcap.isOpened():
        frame_exists, frame = vidcap.read()
        if frame_exists:
            total_number_of_frames += 1
        else:
            break

    vidcap = cv2.VideoCapture(str(path_to_video))

    print(
        f"\nExtracting {total_number_of_frames} frames from {path_to_video} to {target_directory}..."
    )
    print(f"Video frame rate is {fps}")
    for _ in tqdm.tqdm(range(total_number_of_frames)):
        file_name = (
                target_directory
                / f"{f'{frame_prefix}_' if frame_prefix else ''}{str(count).zfill(8)}.png"
        )
        success, image = vidcap.read()
        print(file_name, success)
        cv2.imwrite(str(file_name), image)
        count += 1



def cleanup_tmp_dir():
    try:
        [f.unlink() for f in _tmp_dir_pathlib.glob("*") if f.is_file()]
    except PermissionError:
        prRed(
            f"Error when cleaning up {_tmp_dir_pathlib} "
            f"Check Full Disk Access settings on Mac"
        )


def convert_video_frame_rate(path_to_video, target_fps=30, output_video_path=None):
    if output_video_path is None:
        output_video_path = path_to_video.parents[
                                0] / f"{path_to_video.stem}_{target_fps}fps{path_to_video.suffix}"
    subprocess.check_output(
        ["ffmpeg", "-i", f'{path_to_video}', "-filter:v", f"fps={target_fps}",
         f"{output_video_path}"]
    )
    # -vcodec libx264  -pix_fmt yuv420p
    # -tag:v hvc1
    # -vf format=yuv420p
    # -c:v libx264
    # -c:v copy -c:a copy -tag:v hvc1
    return output_video_path

# function for combined two frames.
def stitch_video_frames(frame1, frame2, Video_w, Video_h, Video_w2, Video_h2):
    frame2 = cv2.resize(frame2, (int(Video_w2), int(Video_h)),
                        interpolation=cv2.INTER_AREA)
    BG = cv2.resize(frame1, (int(Video_w + Video_w2), int(Video_h)),
                    interpolation=cv2.INTER_AREA)
    BG[0:int(Video_h), 0:int(Video_w)] = frame1
    BG[0:int(Video_h), int(Video_w):int(Video_w + Video_w2)] = frame2
    return (BG)



def stitch_list_of_videos_side_by_side(list_of_paths_to_videos,
                                       target_filename,
                                       target_directory,
                                       fps,
                                       insert_subtitle=False):
    target_filename = file_manager.find_new_unique_filename(target_file_path=target_directory/f"{target_filename}.mp4")
    target_file_path = target_directory/ f"{target_filename}.mp4"

    Video1 = list_of_paths_to_videos[0]
    Video2 = list_of_paths_to_videos[1]

    cap1 = cv2.VideoCapture(str(Video1))
    cap2 = cv2.VideoCapture(str(Video2))

    # The video 1 set the video 1 as the default size and fps
    Video_h = cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)
    Video_w = cap1.get(cv2.CAP_PROP_FRAME_WIDTH)
    Video_h2 = cap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
    Video_w2 = cap2.get(cv2.CAP_PROP_FRAME_WIDTH)
    size = (int(Video_w + Video_w2), int(Video_h))

    fps_c = cap1.get(cv2.CAP_PROP_FPS)
    fps_c2 = cap2.get(cv2.CAP_PROP_FPS)
    # else:
    #     size = (int(Window.split("x")[0]), int(Window.split("x")[1]))

    if int(fps_c) != int(fps_c2):
        prRed(f"Warning frame rates differ. {fps_c} vs {fps_c2}. "
              f"Video with highest frame rate will be converted to match the other")

        if fps_c > fps_c2:
            Video1 = convert_video_frame_rate(path_to_video=Video1, target_fps=fps)
            cap1 = cv2.VideoCapture(str(Video1))

        elif fps_c2 > fps_c:
            Video2 = convert_video_frame_rate(path_to_video=Video2, target_fps=fps)
            cap2 = cv2.VideoCapture(str(Video2))

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    videowriter = cv2.VideoWriter(str(target_file_path), fourcc, fps, size)

    while (True):
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()
        if frame1 is None or frame2 is None:
            break

        frame1pil = image_editor.convert_opencv_format_to_pil(frame1)
        frame2pil = image_editor.convert_opencv_format_to_pil(frame2)

        img = stitch_video_frames(frame1, frame2, Video_w, Video_h, Video_w2, Video_h2)
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        videowriter.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    # videowriter.write(frame)
