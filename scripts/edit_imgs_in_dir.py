import argparse
from concurrent import futures
from pathlib import Path

from tqdm import tqdm

import file_manager.file_manager as file_manager
import image_editor


def edit_img(img_path, target_output_dir):
    """Custom method to modify an image as you wish. Since the scope is very broad, you should edit the script and tailor it to your objectives.
    Some examples of the method capabilities:
        - Rotate image
        - Strip EXIF metadata


    :param img_path: Path to input image
    :param target_output_dir: Path to store edited image
    """
    file_name = img_path.stem
    img = image_editor.open_image(img_path)

    # Insert any image operations here
    img = img.rotate(angle=90, expand=True)
    img = image_editor.strip_exif(img)
    img = image_editor.invert(img)

    # Save file
    image_editor.save_img(
        img, target_file_name=file_name, target_directory=target_output_dir
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Manipulate images in a directory")
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing images", type=Path
    )
    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store modified images",
        type=Path,
        default=None,
    )

    args = parser.parse_args()
    target_dir = args.tdir

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_edited"

    file_manager.create_directory(target_dir)

    list_of_files = file_manager.list_all_image_filepaths_in_dir(args.dir)

    with futures.ProcessPoolExecutor() as pool:
        with tqdm(total=len(list_of_files)) as progressbar:
            for _ in pool.map(
                edit_img, list_of_files, [target_dir] * len(list_of_files)
            ):
                progressbar.update(1)
