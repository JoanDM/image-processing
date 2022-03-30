import subprocess

import cv2
import tqdm

import image_editor
from config import (
    _1_minute_timer_video_path,
    _default_font_path,
    _default_subtitle_height_percentage,
    _ffmpeg_path,
    _ffprobe_path,
    _tmp_dir_pathlib,
    pr_red,
)
from file_manager import file_manager


def create_video_from_frames_in_dir(
    path_to_directory,
    target_directory,
    target_video_name,
    fps,
    frames_to_freeze=None,
    freeze_last_frame=False,
    seconds_freezing_frame=2,
    insert_subtitles=False,
):
    """Compose video from frame sequence in directory

    :param path_to_directory: Path to directory with frames
    :param target_directory: Target directory to store composed video
    :param target_video_name: Target name for composed video
    :param fps: Target video frame rate
    :param frames_to_freeze: List of keyframes ids to be frozen, defaults to None
    :param freeze_last_frame: Flag to freeze last frames of the video, defaults to False
    :param seconds_freezing_frame: Time in secods freezing frames, defaults to 2
    :param insert_subtitles: Flag to insert subtitles based on the frame name, defaults to False
    :return: Path to converted video
    """
    file_manager.create_directory(target_directory)
    target_video_path = file_manager.find_new_unique_file_path(
        target_directory / f"{target_video_name}.mp4"
    )

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
    for file_path in tqdm.tqdm(list_of_files, total=len(list_of_files)):
        img = image_editor.open_image(file_path)
        if insert_subtitles:
            image_editor.insert_subtitle(
                img=img,
                text=file_path.stem,
                color="white",
                subtitle_height_percentage=_default_subtitle_height_percentage,
            )

        img = image_editor.convert_pil_to_opencv_format(img=img)

        out.write(img)

        if frames_to_freeze is not None:
            for _ in range(seconds_freezing_frame * fps):
                out.write(img)

    if freeze_last_frame:
        for _ in range(seconds_freezing_frame * fps):
            out.write(img)

    out.release()
    return target_video_path


def extract_frames_from_video(path_to_video, target_directory, frame_prefix=""):
    """Extract frames from video

    :param path_to_video: Path to video
    :param target_directory: Target directory to store extracted frames
    :param frame_prefix: The default naming for the frames is their index, you can define a custom prefix here, defaults to ""
    """
    vidcap = cv2.VideoCapture(str(path_to_video))
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    target_directory = target_directory.parents[0] / f"{target_directory.stem}_{fps}FPS"
    file_manager.create_directory(target_directory)

    count = 0

    # Loop through the video to get the number of frames
    total_number_of_frames = 0
    while vidcap.isOpened():
        frame_exists, _ = vidcap.read()
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
        _, image = vidcap.read()
        cv2.imwrite(str(file_name), image)
        count += 1


def cleanup_tmp_dir():
    """Cleanup tmp folder"""
    try:
        [f.unlink() for f in _tmp_dir_pathlib.glob("*") if f.is_file()]
    except PermissionError:
        pr_red(
            f"Error when cleaning up {_tmp_dir_pathlib} "
            f"Check Full Disk Access settings on Mac"
        )


def convert_video_frame_rate(
    path_to_video, target_directory, target_file_name, target_fps=30
):
    """Convert video frame rate with FFMPEG. This will preserve the actual video speed (will not fast-forward or slow-mo)

    :param path_to_video: Path to video
    :param target_directory: Path to store converted video
    :param target_fps: Expected output video frame rate, defaults to 30
    :return: Path to converted video
    """
    output_video_path = target_directory / target_file_name
    subprocess.check_output(
        [
            _ffmpeg_path,
            "-i",
            f"{path_to_video}",
            "-filter:v",
            f"fps={target_fps}",
            f"{output_video_path}",
        ]
    )
    # -vcodec libx264  -pix_fmt yuv420p
    # -tag:v hvc1
    # -vf format=yuv420p
    # -c:v libx264
    # -c:v copy -c:a copy -tag:v hvc1
    return output_video_path


def get_video_length_in_sec(path_to_video):
    """Get video duration in seconds

    :param path_to_video: Path to video
    :return: Video duration in seconds (float)
    """
    video_length = float(
        subprocess.check_output(
            [
                f"{_ffprobe_path} -v error -select_streams v:0 -show_entries stream=duration -of default=nw=1:nk=1 '{path_to_video}'"
            ],
            shell=True,
        )
    )

    return video_length


def get_video_size(path_to_video):
    """Get video height and width through ffprobe

    :param path_to_video: Path to video
    :return: Tuple (video_w, video_h) in pixels
    """
    video_w = int(
        subprocess.check_output(
            [
                f"{_ffprobe_path} -v error -show_entries stream=width -of default=nw=1:nk=1 '{path_to_video}'"
            ],
            shell=True,
        )
    )
    video_h = int(
        subprocess.check_output(
            [
                f"{_ffprobe_path} -v error -show_entries stream=height -of default=nw=1:nk=1 '{path_to_video}'"
            ],
            shell=True,
        )
    )
    return video_w, video_h


def crop_video(
    path_to_video, target_filename, target_directory, target_width, target_height, x, y
):
    """Crop video through FFMPEG commands

    :param path_to_video: Path to video
    :param target_filename: Target name for cropped video
    :param target_directory: Target directory to store cropped video
    :param target_width: Target final video width
    :param target_height: Target final video height
    :param x: X coordinate for top left corner for cropping box
    :param y: y coordinate for top left corner for cropping box
    """
    target_file_path = file_manager.find_new_unique_file_path(
        target_file_path=target_directory / f"{target_filename}.mp4"
    )
    ffmpeg_crop_str = f"crop={target_width}:{target_height}:{x}:{y}"
    subprocess.check_output(
        [
            f"{_ffmpeg_path} -i {path_to_video} -filter:v '{ffmpeg_crop_str}' '{target_file_path}'"
        ],
        shell=True,
    )


def stitch_list_of_videos_side_by_side(
    list_of_paths_to_videos,
    target_filename,
    target_directory,
    slow_mo_factor,
    last_frame_freeze_duration,
    insert_timers,
    list_of_subtitles,
    remove_audio,
):
    """Create a video composition of side by side videos. The script will construct and execute necessary FFMPEG command line program

    :param list_of_paths_to_videos: List ot paths to videos to stitch together, sorted from left to right
    :param target_filename: Target name for the composition
    :param target_directory: Target directory to store video composition
    :param slow_mo_factor: Factor for video slow-down
    :param last_frame_freeze_duration: How long should the last composition frame stay frozen
    :param insert_timers: Insert a timer at the top-left side of every video
    :param list_of_subtitles: List of subtitles to set below every video
    :param remove_audio: Remove audio from final composition
    """
    max_duration = 0
    duration_list = []
    ffmpeg_input_videos = ""
    # Final composition height is based on first video size
    _, final_video_h = get_video_size(list_of_paths_to_videos[0])

    # Examine input videos
    for video_path in list_of_paths_to_videos:
        # Construct FFMPEG command for input videos
        ffmpeg_input_videos += f"-i '{video_path}' "
        # Collect the video lenghts to properly trim and cut composition
        vid_duration = get_video_length_in_sec(video_path)
        duration_list.append(vid_duration)
        max_duration = (
            max(max_duration, vid_duration)
            + last_frame_freeze_duration / slow_mo_factor
        )

    # The following actions are done by constructing FFMPEG complex filters
    ffmpeg_complex_filter = ""

    # Video scaling
    for i in range(len(list_of_paths_to_videos)):
        # All videos must be scaled to match first input video height
        ffmpeg_complex_filter += f"[{i}:v]scale=-1:{final_video_h}[v{i}];"
        if insert_timers:
            # Scale and set durations for timers
            timer_height = int(final_video_h * _default_subtitle_height_percentage)
            ffmpeg_input_videos += f" -i '{_1_minute_timer_video_path}'"
            ffmpeg_complex_filter += f"[{len(list_of_paths_to_videos) + i}:v]scale=-1:{timer_height}[timer{i}];[timer{i}]trim=duration={duration_list[i]}[timer{i}];"

    # Construct the horizontal video stack layout with padding inbetween videos
    padding_width = 20
    ffmpeg_stack_filter = ""
    for i in range(len(list_of_paths_to_videos) - 1):
        ffmpeg_complex_filter += f"color=black:{padding_width}x{final_video_h}:d={max_duration}[blackpad{i}];"
        ffmpeg_stack_filter += f"[v{i}][blackpad{i}]"
    i += 1
    ffmpeg_stack_filter += (
        f"[v{i}]hstack=inputs={len(list_of_paths_to_videos)*2-1}[composition];"
    )
    ffmpeg_complex_filter += ffmpeg_stack_filter

    # Insert a black banner at the bottom of the composition and insert video subtitles
    # to identify every single input video

    text_box_opacity = 1.0
    text_height_percentage = _default_subtitle_height_percentage
    ffmpeg_complex_filter += f"[composition]drawbox=x=0:y=ih-h:w=iw:h=ih*{text_height_percentage}:color=black@{text_box_opacity}:t=fill"
    normalized_font_size = 1000
    for i, subtitle_text in enumerate(list_of_subtitles):
        input_video_w, input_video_h = get_video_size(list_of_paths_to_videos[i])
        # If input video had to be rescaled, find resulting w after scaling

        subtitle_text = subtitle_text.replace(" ", "\ ")
        if input_video_h != final_video_h:
            input_video_w = input_video_w / input_video_h * final_video_h
        font_size = image_editor.find_best_font_size(
            subtitle_text, input_video_w, text_height_percentage * final_video_h
        )
        normalized_font_size = min(normalized_font_size, font_size)
    video_width_tracker = 0
    for i, subtitle_text in enumerate(list_of_subtitles):
        subtitle_text = subtitle_text.replace(" ", "\ ")
        ffmpeg_complex_filter += f",drawtext=fontfile={_default_font_path}:text='{subtitle_text}':fontcolor=white:fontsize={normalized_font_size}:x={video_width_tracker}+{input_video_w}/2-text_w/2:y=h-text_h-10"
        video_width_tracker += input_video_w + padding_width

    if insert_timers:
        video_width_tracker = 0
        for i in range(len(list_of_paths_to_videos) - 1):
            ffmpeg_complex_filter += f"[composition];[composition][timer{i}]overlay={video_width_tracker}:{0}[composition]"

            input_video_w, input_video_h = get_video_size(list_of_paths_to_videos[i])
            video_width_tracker += input_video_w + padding_width
        i += 1
        ffmpeg_complex_filter += (
            f";[composition][timer{i}]overlay={video_width_tracker}:{0}"
        )

    # Slow down the final composition by x factor
    if slow_mo_factor and not remove_audio:
        ffmpeg_complex_filter += (
            f"[composition];[composition]setpts={float(slow_mo_factor)}*PTS"
        )
        if slow_mo_factor <= 2:
            ffmpeg_complex_filter += f";amix=inputs={len(list_of_paths_to_videos)},atempo={float(1/slow_mo_factor)}"
            audio_option = "-ac 2"
        else:
            pr_red(
                "Warning, slow mo factor is greater than two, audio will be removed since it's not possible to slow down >2"
            )
            audio_option = "-an"
    else:
        ffmpeg_complex_filter += f";amix=inputs={len(list_of_paths_to_videos)}"
        audio_option = "-ac 2"

    target_file_path = file_manager.find_new_unique_file_path(
        target_file_path=target_directory / f"{target_filename}.mp4"
    )
    # -ac 2 to downmix audio to stereo
    subprocess.check_output(
        [
            f"{_ffmpeg_path} {ffmpeg_input_videos} -filter_complex '{ffmpeg_complex_filter}' {audio_option} -vsync 0 '{target_file_path}'"
        ],
        shell=True,
    )


# # function for combined two frames.
# def stitch_video_frames_opencv(frame1, frame2, Video_w, Video_h, Video_w2, Video_h2):
#     frame2 = cv2.resize(
#         frame2, (int(Video_w2), int(Video_h)), interpolation=cv2.INTER_AREA
#     )
#     BG = cv2.resize(
#         frame1, (int(Video_w + Video_w2), int(Video_h)), interpolation=cv2.INTER_AREA
#     )
#     BG[0 : int(Video_h), 0 : int(Video_w)] = frame1
#     BG[0 : int(Video_h), int(Video_w) : int(Video_w + Video_w2)] = frame2
#     return BG


# def stitch_list_of_videos_side_by_side_opencv(
#     list_of_paths_to_videos,
#     target_filename,
#     target_directory,
#     fps,
#     list_of_subtitles=None,
# ):
#     """Open CV version of the video stitching method. Much slower than the ffmpeg version but more readable

#     :param list_of_paths_to_videos: List ot paths to videos to stitch together, sorted from left to right
#     :param target_filename: Target name for the composition
#     :param target_directory: Target directory to store video composition
#     :param fps: Target frame rate for final video composition
#     :param list_of_subtitles: List of subtitles to set below every video, defaults to None
#     """
#     target_file_path = file_manager.find_new_unique_file_path(
#         target_file_path=target_directory / f"{target_filename}.mp4"
#     )

#     Video1 = list_of_paths_to_videos[0]
#     Video2 = list_of_paths_to_videos[1]

#     cap1 = cv2.VideoCapture(str(Video1))
#     cap2 = cv2.VideoCapture(str(Video2))

#     # fps_c = cap1.get(cv2.CAP_PROP_FPS)
#     # fps_c2 = cap2.get(cv2.CAP_PROP_FPS)

#     Video1 = convert_video_frame_rate(
#         path_to_video=Video1,
#         target_fps=_default_frame_rate,
#         target_directory=target_directory,
#         target_file_name=f"{Video1.stem}_{_default_frame_rate}fps{Video1.suffix}",
#     )
#     cap1 = cv2.VideoCapture(str(Video1))

#     Video2 = convert_video_frame_rate(
#         path_to_video=Video2,
#         target_fps=_default_frame_rate,
#         target_directory=target_directory,
#         target_file_name=f"{Video2.stem}_{_default_frame_rate}fps{Video2.suffix}",
#     )
#     cap2 = cv2.VideoCapture(str(Video2))

#     num_frames_vid1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
#     num_frames_vid2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))

#     fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
#     videowriter = None

#     for i in tqdm.tqdm(range(max(num_frames_vid1, num_frames_vid2))):
#         # ret, frame1 = cap1.read()
#         # ret, frame2 = cap2.read()

#         if i < num_frames_vid1:
#             ret, frame1 = cap1.read()

#         if i < num_frames_vid2:
#             ret, frame2 = cap2.read()

#         if i == (max(num_frames_vid1, num_frames_vid2)):
#             break

#         frame1pil = image_editor.convert_opencv_format_to_pil(frame1)
#         frame2pil = image_editor.convert_opencv_format_to_pil(frame2)
#         if list_of_subtitles:
#             image_editor.insert_subtitle(img=frame1pil, text=list_of_subtitles[0])
#             image_editor.insert_subtitle(img=frame2pil, text=list_of_subtitles[1])

#         img = image_editor.stitch_images_side_by_side([frame1pil, frame2pil])
#         if videowriter is None:
#             size = img.size
#             videowriter = cv2.VideoWriter(str(target_file_path), fourcc, fps, size)
#         img = image_editor.convert_pil_to_opencv_format(img)

#         videowriter.write(img)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             cv2.destroyAllWindows()
#             break

#     # file_manager.move_file_to_trash(Video1)
#     # file_manager.move_file_to_trash(Video2)
