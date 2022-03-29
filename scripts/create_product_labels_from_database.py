import image_editor
from config import (
    _a4_pixel_height_default_dpi,
    _a4_pixel_width_default_dpi,
    _default_dpi,
    _resources_dir_pathlib,
    _results_dir_pathlib,
)
from data_processing.data_processsor_class import CsvDataProcessor


def create_product_labels(
    target_directory,
    target_file_name,
    product_names,
    product_models,
    product_serial_numbers,
    img_format="bmp",
):
    """Create printable labels with QR codes to identify products in a database.

    :param target_directory: Path to store created labels
    :param target_file_name: Name for the created file with labels without suffix
    :param product_names: List of product names
    :param product_models: List of product models
    :param product_serial_numbers: List of product serial numbers
    :param img_format: Image format to save created labels, defaults to "bmp"
    """
    # Specify label width and height
    label_width_cm, label_height_cm = (8, 3)
    label_width_inch, label_height_inch = (
        label_width_cm / 2.54,
        label_height_cm / 2.54,
    )

    label_width_px = int(_default_dpi * label_width_inch)
    label_height_px = int(_default_dpi * label_height_inch)

    max_label_rows = int(_a4_pixel_height_default_dpi / label_height_px)
    max_label_cols = int(_a4_pixel_width_default_dpi / label_width_px)

    # Create grid of labels, create additional files if they don't fit in a single A4
    i = 0
    j = 0
    for index in len(product_names):
        if i == 0 and j == 0:
            product_labels_img = image_editor.create_blank_image(
                size=(_a4_pixel_width_default_dpi, _a4_pixel_height_default_dpi)
            )

        if i == max_label_rows:
            j += 1
            i = 0
        if j == max_label_cols:
            j = 0
            i = 0
            image_editor.save_img(
                img=product_labels_img,
                target_file_name=target_file_name,
                target_directory=target_directory,
                img_format=img_format,
                dpi=(_default_dpi, _default_dpi),
            )

        # Draw label rectangle
        image_editor.insert_rectangle(
            img=product_labels_img,
            rectangle_fill_color="white",
            position=(j * label_width_px, i * label_height_px),
            rectangle_height=label_height_px,
            rectangle_width=label_width_px,
            outline_color="black",
            outline_width=2,
        )

        # Create text field with product name, model and serial_number
        product_name = product_names[index]
        product_model = product_models[index]
        product_serial_number = product_serial_numbers[index]
        max_text_width_pix = int(label_width_px * 0.75)
        offset_from_label_corners = int(label_width_px * 0.02)
        image_editor.insert_text(
            img=product_labels_img,
            text=f"{product_name}\n\nModel: {product_model}\nSN:{product_serial_number}",
            color="black",
            position=(
                j * label_width_px + offset_from_label_corners,
                i * label_height_px + offset_from_label_corners,
            ),
            max_width_pix=max_text_width_pix,
            max_height_pix=label_height_px,
        )

        # Create QR code to serve as unique product identifier
        qr_img = image_editor.create_qr_code_image(
            code_content=f"{product_serial_number}"
        )

        desired_qr_code_width_pix = (label_width_px - max_text_width_pix) * 0.8

        qr_code_w, _ = qr_img.size

        barcode_resizing_factor = desired_qr_code_width_pix / qr_code_w

        image_editor.paste_img(
            main_img=product_labels_img,
            img_to_paste=qr_img,
            position=(
                j * label_width_px
                + max_text_width_pix
                + offset_from_label_corners
                + int(desired_qr_code_width_pix / 2),
                i * label_height_px + int(label_height_px / 2),
            ),
            resizing_factor=barcode_resizing_factor,
            anchor_point="center",
        )

        i += 1
    image_editor.save_img(
        img=product_labels_img,
        target_file_name=target_file_name,
        target_directory=target_directory,
        img_format=img_format,
        dpi=(_default_dpi, _default_dpi),
    )


if __name__ == "__main__":
    dataprocessor = CsvDataProcessor(_results_dir_pathlib)
    dataprocessor.fetch_csv_data_from_file_into_dataframe(
        _resources_dir_pathlib / "example_product_database.csv"
    )

    target_directory = _results_dir_pathlib
    target_filename = "example_product_labels"
    product_names = dataprocessor.get_list_of_all_elements_in_column("Product Name")
    product_models = dataprocessor.get_list_of_all_elements_in_column("Product Model")
    product_serial_numbers = dataprocessor.get_list_of_all_elements_in_column(
        "Product Serial Number"
    )

    create_product_labels(
        target_directory,
        target_filename,
        product_names,
        product_models,
        product_serial_numbers,
    )
