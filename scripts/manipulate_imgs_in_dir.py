import image_editor
from concurrent import futures
from tqdm import tqdm
import argparse
import file_manager
from pathlib import Path


def manipulate_img(img_path, target_output_dir=None):
    file_name = img_path.stem
    img = image_editor.open_image(img_path)

    # Insert any image operations here
    img = image_editor.rotate(img, angle_deg=90)
    img = image_editor.strip_exif(img)

    # Save file
    image_editor.save_img(img,
                          target_file_name=file_name,
                          target_directory=target_output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        "Manipulate images in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing images", type=Path
    )
    parser.add_argument("-tdir", nargs="?", help="Target dir to store composition",
                        type=Path, default=None)

    args = parser.parse_args()
    target_dir = args.tdir

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_edited"

    file_manager.create_directory(target_dir)

    list_of_files = file_manager.list_all_image_filepaths_in_dir(args.dir)

    with futures.ProcessPoolExecutor() as pool:
        with tqdm(total=len(list_of_files)) as progressbar:
            for _ in pool.map(manipulate_img, list_of_files,
                              [target_dir]*len(list_of_files)):
                progressbar.update(1)
