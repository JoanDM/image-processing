from pathlib import Path

import cv2
import tqdm
from PIL import Image, ImageDraw, ImageFont

from config import _results_dir_pathlib


class ImageEditor(object):
    def __init__(self, target_directory):
        self.set_target_directory(target_directory)
        self.current_img = None
        self.current_img_path = None

    def set_target_directory(self, target_directory):
        self.target_directory = Path(str(target_directory))
        target_directory.mkdir(parents=True, exist_ok=True)

    def set_current_img(self, path_to_image):
        self.current_img_path = path_to_image
        self.current_img = Image.open(path_to_image)

    def save_current_img(self, target_file_name):
        target_file_path = (
            self.target_directory / f"{target_file_name}{self.current_img_path.suffix}"
        )
        self.current_img.save(target_file_path)

    def insert_rectangle_to_image(
        self,
        rectangle_fill_color="black",
        x_coord=None,
        y_coord=None,
        rectangle_height=None,
        rectangle_width=None,
        outline_color=None,
        outline_width=None,
    ):
        # X is the horizontal axis, top left corner of the picture is 0
        # Y is the vertical axis, top left corner of the picture is 0
        draw = ImageDraw.Draw(self.current_img)
        draw.rectangle(
            xy=(
                x_coord,
                y_coord,
                x_coord + rectangle_width,
                y_coord + rectangle_height,
            ),
            fill=rectangle_fill_color,
            outline=outline_color,
            width=outline_width,
        )

    def insert_text_to_image(self, text=None, color="white", size=100):
        draw = ImageDraw.Draw(self.current_img)

        font = ImageFont.truetype("/Library/fonts/Arial.ttf", size)
        draw.text((10, 10), text, color, font=font)

    def resize_image(self, size):

        self.current_img.thumbnail(size, Image.ANTIALIAS)

    def extract_frames_from_video(self, path_to_video, frame_prefix=""):

        vidcap = cv2.VideoCapture(str(path_to_video))

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
            f"\nExtracting {total_number_of_frames} frames from {path_to_video} to {self.target_directory}..."
        )
        for _ in tqdm.tqdm(range(total_number_of_frames)):
            file_name = (
                self.target_directory
                / f"{f'{frame_prefix}_' if frame_prefix else ''}{str(count).zfill(4)}.png"
            )
            success, image = vidcap.read()
            cv2.imwrite(str(file_name), image)
            count += 1


if __name__ == "__main__":
    img_path = Path(
        "/Users/joandomenech/terry-the-robot/captured_images/2021-10-19/ios/fixed_focus_sharp_seq copy"
    )

    target_path = _results_dir_pathlib / "test_res"

    editor = ImageEditor(target_path)

    editor.set_current_img(img_path)

    editor.insert_rectangle_to_image(
        x_coord=0, y_coord=0, rectangle_height=300, rectangle_width=700
    )

    editor.insert_text_to_image(text=f"Frame #200\n2.333 seconds")

    editor.save_current_img(target_file_name="test")
