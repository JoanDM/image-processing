import cv2
import numpy
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps

import file_manager.file_manager as file_manager
from config import _default_subtitle_height_percentage


def open_image(path_to_img):
    """Open image with PIL

    :param path_to_img: Path to img
    :return: PIL instance of image
    """
    return Image.open(path_to_img)


def create_blank_image(size=(1, 1)):
    """Create plain white image with PIL

    :param size: Tuple for x,y size in pixels, defaults to (1, 1)
    :return: PIL instance of plain white image
    """
    return Image.new("RGB", size, (255, 255, 255))


def convert_pil_to_opencv_format(img):
    """Convert PIL instance of an img to OpenCV-compatible (based on NumPy)

    :param img: PIL instance of image
    :return: OpenCV-compatible instance of image (based on NumPy)
    """
    pil_img = img.convert("RGB")
    img = numpy.array(pil_img)
    return img[:, :, ::-1].copy()


def convert_opencv_format_to_pil(img):
    """Convert OpenCV-compatible instance of an image to PIL

    :param img: OpenCV-compatible instance of image
    :return: PIL instance of image
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def strip_exif(img):
    """Strip EXIF metadata from image

    :param img: PIL instance of image
    :return: PIL instance of image with stripped EXIF
    """
    data = img.getdata()
    img = Image.new(img.mode, img.size)
    img.putdata(data)
    return img


def save_img(
    img, target_file_name, target_directory, dpi=None, img_format="png", overwrite=False
):
    """Save PIL instance of an image

    :param img: PIL instance of an image
    :param target_file_name: Target name for input image, without suffix
    :param target_directory: Path to store image
    :param dpi: Target dots per inch, defaults to None
    :param img_format: Target file format, defaults to "png"
    :param overwrite: Flag to select file overwriting, defaults to False
    """
    target_file_path = target_directory / f"{target_file_name}.{img_format}"
    if target_file_path.exists() and not overwrite:
        target_file_path = file_manager.find_new_unique_file_path(target_file_path)

    img.save(target_file_path, dpi=dpi)


def invert(img):
    """Invert image

    :param img: PIL instance of image
    :return: PIL instance of inverted image
    """
    return ImageOps.invert(img)


def insert_rectangle(
    img,
    position,
    rectangle_height,
    rectangle_width,
    rectangle_fill_color="black",
    anchor_point="top_left",
    outline_color=None,
    outline_width=None,
):
    """Insert an opaque rectangle to PIL image

    :param img: PIL instance of image
    :param position: Tuple x,y for rectangle position
    :param rectangle_height: Rectangle height in pixels
    :param rectangle_width: Rectangle width in pixels
    :param rectangle_fill_color: defaults to "black"
    :param anchor_point: Anchor point for rectangle positioning, defaults to "top_left"
    :param outline_color: defaults to None
    :param outline_width: defaults to None
    """
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
    """Insert text on PIL image

    :param img: PIL instance of image
    :param text: String to insert
    :param position: Tuple X, Y for text position_
    :param max_width_pix: Maximum text width allowed in pixels
    :param max_height_pix: Maximum text height allowed in pixels
    :param color: defaults to "white"
    :param anchor_point: Anchor point for text positioning, defaults to "top_left"
    """
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
    box_color="black",
    text_color="white",
    anchor_point="top_left",
):
    """Combination of rectangle + text insertion to a PIL image in one method

    :param img: PIL instance of image
    :param text: String to insert
    :param position: Tuple X,Y for text box positioning
    :param box_width: Box width in pixels
    :param box_height: Box height in pixels
    :param box_color: defaults to "black"
    :param text_color: defaults to "white"
    :param anchor_point: Anchor point for text box positioning, defaults to "top_left"
    """
    insert_rectangle(
        img=img,
        rectangle_fill_color=box_color,
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
        color=text_color,
        max_width_pix=box_width * 0.8,
        max_height_pix=box_height * 0.8,
        position=text_position,
        anchor_point=anchor_point,
    )


def insert_subtitle(
    img,
    text,
    color="white",
    subtitle_height_percentage=_default_subtitle_height_percentage,
):
    """Insert subtitle to PIL image, by default a black background covering all image width will be introduced

    :param img: PIL instance of image
    :param text: String to insert
    :param color: defaults to "white"
    :param subtitle_height_percentage: Height percentage of the image occupied as a subtitle overlay, defaults to _default_subtitle_height_percentage
    """
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


def stitch_images_side_by_side(list_of_imgs, list_of_subtitles=None):
    """Stitch images side by side based on the first image's height

    :param list_of_imgs: List of PIL instances of images
    :param list_of_subtitles: List of subtitles to be inserted on every stitched image, if None, no subtitle will be introduced. Defaults to None
    :return: PIL instance of image composition
    """
    first_img = list_of_imgs[0]
    first_img_size = first_img.size
    total_size = [first_img_size[0], first_img_size[1]]
    for img in list_of_imgs[1:]:
        img_size = img.size
        if img_size[1] != total_size[1]:
            total_size[0] += int((img_size[0] / img_size[1]) * total_size[1])
        else:
            total_size[0] += img_size[0]

    comp_img = create_blank_image(tuple(total_size))

    x_size_tracker = 0
    for i, next_img in enumerate(list_of_imgs):
        next_img_size = next_img.size
        if next_img_size[1] != total_size[1]:
            next_img = next_img.resize(
                size=(
                    int(next_img_size[0] / next_img_size[1] * total_size[1]),
                    int(total_size[1]),
                )
            )
        if list_of_subtitles:
            insert_subtitle(next_img, list_of_subtitles[i])

        comp_img.paste(next_img, (x_size_tracker, 0))
        x_size_tracker += next_img.size[0]

    return comp_img


def paste_img(
    main_img, img_to_paste, position, anchor_point="center", resizing_factor=1
):
    """Paste img on PIL instance of an image

    :param main_img: PIL instance of base image
    :param img_to_paste: PIL instance of image to be pasted
    :param position: Tuple X,Y for pasted image positioning
    :param anchor_point: Anchor point for pasted image positioning, defaults to "center"
    :param resizing_factor: _description_, defaults to 1
    """
    img_w, img_h = img_to_paste.size
    img_to_paste = img_to_paste.resize(
        (int(img_h * resizing_factor), int(img_h * resizing_factor))
    )
    img_w, img_h = img_to_paste.size
    offset = (0, 0)
    if anchor_point == "center":
        offset = [-img_w // 2, -img_h // 2]
    position = [x + y for x, y in zip(offset, position)]
    main_img.paste(img_to_paste, position)


def create_qr_code_image(code_content):
    """Create QR code instance

    :param code_content: String with content to encrypt into QR
    :return: PIL instance of QR code
    """
    return qrcode.make(code_content)


def find_best_font_size(text, max_width_pix, max_height_pix):
    # Initialize font size
    font_size = 100
    from config import _default_font_path

    font = ImageFont.truetype(str(_default_font_path), font_size)

    w, h = font.getsize(text)
    # This value would override the font size
    while h >= max_height_pix:
        font_size -= 1
        font = ImageFont.truetype(str(_default_font_path), font_size)
        w, h = font.getsize(text)

    while h <= max_height_pix:
        font_size += 1
        font = ImageFont.truetype(str(_default_font_path), font_size)
        w, h = font.getsize(text)

    if w > max_width_pix:
        text_fits_in_rectangle = False
    else:
        text_fits_in_rectangle = True

    if not text_fits_in_rectangle:
        while w >= max_width_pix:
            font_size -= 1
            font = ImageFont.truetype(str(_default_font_path), font_size)
            w, h = font.getsize(text)

        while w <= max_width_pix:
            font_size += 1
            font = ImageFont.truetype(str(_default_font_path), font_size)
            w, h = font.getsize(text)

    return font_size
