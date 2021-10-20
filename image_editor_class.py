from pathlib import Path

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
