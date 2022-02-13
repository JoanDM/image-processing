from pathlib import Path
import argparse
import image_editor
import file_manager

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create an image composition by stitching images in a directory"
    )
    parser.add_argument(
        "-dir", nargs="?", help="Directory containing images", type=Path
    )
    parser.add_argument("-tdir", nargs="?", help="Target dir to store composition",
                        type=Path, default=None)

    parser.add_argument("-fname", nargs="?", help="name for the composition", type=str)

    args = parser.parse_args()
    target_dir = args.tdir
    file_name = args.fname

    if target_dir is None:
        target_dir = args.dir.parents[0] / f"{args.dir.stem}_comp"
        file_manager.create_directory(target_dir)

    if file_name is None:
        file_name = args.dir.stem

    list_of_paths_to_images = file_manager.list_all_image_filepaths_in_dir(args.dir)

    comp = image_editor.stitch_images_side_by_side(
        list_of_paths_to_images=list_of_paths_to_images,
        insert_subtitles=True)

    image_editor.save_img(img=comp, target_file_name=file_name,
                          target_directory=target_dir)
