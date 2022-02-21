import argparse
from pathlib import Path

import file_manager.file_manager as file_manager
import image_editor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create an image composition by stitching images in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing images", type=Path
    )
    parser.add_argument(
        "-tdir",
        nargs="?",
        help="Target dir to store composition",
        type=Path,
        default=None,
    )

    parser.add_argument("-fname", nargs="?", help="name for the composition", type=str)
    parser.add_argument("-nosubs", help="insert img subtitles", action="store_true")

    args = parser.parse_args()
    target_dir = args.tdir
    file_name = args.fname

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_comp"
        file_manager.create_directory(target_dir)

    if file_name is None:
        file_name = args.dir.stem

    list_of_imgs = []

    for img_path in file_manager.list_all_image_filepaths_in_dir(args.dir):
        list_of_imgs.append(image_editor.open_image(img_path))
    if args.nosubs:
        list_of_subtitles = None
    else:
        list_of_subtitles = file_manager.list_all_image_filenames_in_dir(args.dir)

    comp = image_editor.stitch_images_side_by_side(
        list_of_imgs=list_of_imgs, list_of_subtitles=list_of_subtitles
    )

    image_editor.save_img(
        img=comp, target_file_name=file_name, target_directory=target_dir
    )
