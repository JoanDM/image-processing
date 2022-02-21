import cv2
import numpy
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps

import file_manager.file_manager as file_manager
from config import DEFAULT_SUBTITLE_HEIGHT_PERCENTAGE


def open_image(path_to_img):
    return Image.open(path_to_img)


def create_blank_image(size=(1, 1)):
    return Image.new("RGB", size, (255, 255, 255))


def convert_pil_to_opencv_format(img):
    pil_img = img.convert("RGB")
    img = numpy.array(pil_img)
    return img[:, :, ::-1].copy()


def convert_opencv_format_to_pil(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def strip_exif(img):
    data = img.getdata()
    img = Image.new(img.mode, img.size)
    img.putdata(data)
    return img


def save_img(
    img, target_file_name, target_directory, dpi=None, img_format="png", overwrite=False
):
    target_file_path = target_directory / f"{target_file_name}.{img_format}"
    if target_file_path.exists() and not overwrite:
        target_file_path = file_manager.find_new_unique_file_path(target_file_path)

    img.save(target_file_path, dpi=dpi)


def get_size(img):
    return img.size


def rotate(img, angle_deg, expand=True):  # counterclockwise rotation
    return img.rotate(angle_deg, expand=expand)


def resize(img, size):
    return img.resize(size, Image.ANTIALIAS)


def invert(img):
    return ImageOps.invert(img)


def insert_rectangle(
    img,
    rectangle_fill_color="black",
    anchor_point="top_left",
    position=None,
    rectangle_height=None,
    rectangle_width=None,
    outline_color=None,
    outline_width=None,
):
    # X is the horizontal axis, top left corner of the picture is 0
    # Y is the vertical axis, top left corner of the picture is 0
    draw = ImageDraw.Draw(img)
    if anchor_point == "bottom_left":
        offset = [0, -rectangle_height]
        position = [x + y for x, y in zip(offset, position)]

    draw.rectangle(
        xy=(
            position[0],
            position[1],
            position[0] + rectangle_width,
            position[1] + rectangle_height,
        ),
        fill=rectangle_fill_color,
        outline=outline_color,
        width=outline_width,
    )


def insert_text(
    img,
    text,
    position,
    max_width_pix,
    max_height_pix,
    color="white",
    anchor_point="top_left",
):
    draw = ImageDraw.Draw(img)

    # Initialize font size
    font_size = 100
    font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)

    w, h = draw.textsize(text, font)
    # This value would override the font size
    while h >= max_height_pix:
        font_size -= 1
        font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)
        w, h = draw.textsize(text, font)

    while h <= max_height_pix:
        font_size += 1
        font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)
        w, h = draw.textsize(text, font)

    if w > max_width_pix:
        text_fits_in_rectangle = False
    else:
        text_fits_in_rectangle = True

    if not text_fits_in_rectangle:
        while w >= max_width_pix:
            font_size -= 1
            font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)
            w, h = draw.textsize(text, font)

        while w <= max_width_pix:
            font_size += 1
            font = ImageFont.truetype("/Library/fonts/Arial.ttf", font_size)
            w, h = draw.textsize(text, font)

    offset = (0, 0)
    if anchor_point == "center":
        offset = [-w // 2, -h // 2]
    position = [x + y for x, y in zip(offset, position)]

    if anchor_point == "bottom_left":
        offset = [0, -h]
        position = [x + y for x, y in zip(offset, position)]

    draw.text(xy=position, text=text, fill=color, font=font)


def insert_text_box(
    img,
    text,
    position,
    box_width,
    box_height,
    color="white",
    anchor_point="top_left",
    insert_subtitle=False,
):
    insert_rectangle(
        img=img,
        rectangle_fill_color="black",
        position=position,
        rectangle_height=box_height,
        rectangle_width=box_width,
        anchor_point=anchor_point,
    )
    img_w, img_h = img.size
    quiet_zone_w = img_w * 0.01
    quiet_zone_h = img_h * 0.01
    text_position = [position[0] + quiet_zone_w, position[1] + quiet_zone_h]
    insert_text(
        img=img,
        text=text,
        color=color,
        max_width_pix=box_width * 0.8,
        max_height_pix=box_height * 0.8,
        position=text_position,
        anchor_point=anchor_point,
    )


def insert_subtitle(
    img,
    text,
    color="white",
    subtitle_height_percentage=DEFAULT_SUBTITLE_HEIGHT_PERCENTAGE,
):
    position = [0, img.size[1]]
    anchor_point = "bottom_left"
    rectangle_height = img.size[1] * subtitle_height_percentage
    rectangle_width = img.size[0]

    insert_rectangle(
        img=img,
        rectangle_fill_color="black",
        position=position,
        rectangle_height=rectangle_height,
        rectangle_width=rectangle_width,
        anchor_point=anchor_point,
    )

    img_w, img_h = img.size
    # quiet_zone_w = img_w * 0.01
    quiet_zone_h = img_h * 0.005

    text_position = [img_w / 2, img_h - rectangle_height / 2 - quiet_zone_h]
    anchor_point = "center"
    insert_text(
        img=img,
        text=text,
        color=color,
        max_width_pix=rectangle_width * 0.8,
        max_height_pix=rectangle_height * 0.8,
        position=text_position,
        anchor_point=anchor_point,
    )


def stitch_images_side_by_side(list_of_paths_to_images, insert_subtitles=False):
    first_img = open_image(list_of_paths_to_images[0])

    first_img_size = first_img.size
    total_size = [first_img_size[0], first_img_size[1]]
    for img_pth in list_of_paths_to_images[1:]:
        img = open_image(img_pth)
        img_size = img.size
        if img_size[1] != total_size[1]:
            total_size[0] += int(total_size[1] / img_size[1] * img_size[0])
        else:
            total_size[0] += img_size[0]

    comp_img = create_blank_image(tuple(total_size))

    x_size_tracker = 0
    for img_pth in list_of_paths_to_images:
        next_img = open_image(img_pth)
        next_img_size = next_img.size
        if next_img_size[1] != total_size[1]:
            next_img = next_img.resize(
                (
                    int(total_size[1] / next_img_size[1] * next_img_size[0]),
                    int(total_size[1]),
                )
            )
        if insert_subtitles:
            insert_subtitle(
                img=next_img,
                text=img_pth.stem,
                color="white",
                subtitle_height_percentage=DEFAULT_SUBTITLE_HEIGHT_PERCENTAGE,
            )
        comp_img.paste(next_img, (x_size_tracker, 0))
        x_size_tracker += next_img.size[0]

    return comp_img


def paste_img(
    main_img, img_to_paste, position, anchor_point="center", resizing_factor=1
):
    img_w, img_h = img_to_paste.size
    img_to_paste = img_to_paste.resize(
        (int(img_h * resizing_factor), int(img_h * resizing_factor))
    )
    img_w, img_h = img_to_paste.size
    offset = (0, 0)
    if anchor_point == "center":
        offset = [-img_w // 2, -img_h // 2]
    position = [x + y for x, y in zip(offset, position)]
    return main_img.paste(img_to_paste, position)


def create_qr_code_image(code_content):
    return qrcode.make(code_content)
