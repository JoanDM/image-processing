from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import _tmp_dir_pathlib, prRed


class ImageEditor(object):
    def __init__(self, target_directory):
        self.set_target_directory(target_directory)
        self.current_img = None
        self.current_img_path = None
        self.current_img_name = None

    def set_target_directory(self, target_directory):
        self.target_directory = Path(str(target_directory))
        target_directory.mkdir(parents=True, exist_ok=True)

    def set_current_img(self, path_to_image):
        self.current_img_path = path_to_image
        self.current_img = Image.open(path_to_image)
        self.current_img_name = self.current_img_path.stem

    def create_and_set_blank_image_as_current(self):
        self.current_img = Image.new("RGB", (1, 1), (250, 250, 250))
        self.current_img_path = self.target_directory / f"new_blank_image.png"
        self.current_img_name = self.current_img_path.stem

    def save_current_img(self, target_file_name):
        target_file_path = (
            self.target_directory / f"{target_file_name}{self.current_img_path.suffix}"
        )
        self.current_img.save(target_file_path)

    def insert_rectangle_to_current_img(
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

    def insert_text_to_current_img(
        self,
        text=None,
        color="white",
        font_size=100,
        position=(10, 10),
        use_black_background=False,
    ):
        draw = ImageDraw.Draw(self.current_img)

        font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)

        if use_black_background:
            quiet_zone = 50
            w, h = draw.textsize(text, font)

            self.insert_rectangle_to_current_img(
                rectangle_fill_color="black",
                x_coord=position[0] - quiet_zone,
                y_coord=position[1] - quiet_zone,
                rectangle_height=h + quiet_zone * 2,
                rectangle_width=w + quiet_zone * 2,
            )

        draw.text(position, text, color, font=font)

    def resize_current_image(self, size):

        self.current_img = self.current_img.resize(size, Image.ANTIALIAS)

    def cleanup_tmp_dir(self):
        try:
            [f.unlink() for f in _tmp_dir_pathlib.glob("*") if f.is_file()]
        except PermissionError:
            prRed(
                f"Error when cleaning up {_tmp_dir_pathlib} "
                f"Check Full Disk Access settings on Mac"
            )

    def create_side_by_side_image_composition(
        self, path_to_left_side_image, path_to_right_side_image
    ):

        image1 = Image.open(path_to_left_side_image)
        image2 = Image.open(path_to_right_side_image)

        image1_size = image1.size

        self.resize_current_image((2 * image1_size[0], image1_size[1]))

        self.current_img.paste(image1, (0, 0))
        self.current_img.paste(image2, (image1_size[0], 0))
