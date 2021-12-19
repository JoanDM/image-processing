from config import (
    A4_PIXEL_HEIGHT_DEFAULT_DPI,
    A4_PIXEL_WIDTH_DEFAULT_DPI,
    DEFAULT_DPI,
    _resources_dir_pathlib,
    _results_dir_pathlib,
    _tmp_dir_pathlib,
)
from data_processing.data_processsor_class import DataProcessor
from image_editor_class import ImageEditor


def create_product_labels(
    target_directory,
    target_file_name,
    product_names,
    product_models,
    product_serial_numbers,
):

    # Specify label width and height
    label_width_cm, label_height_cm = (8, 3)
    label_width_inch, label_height_inch = (
        label_width_cm / 2.54,
        label_height_cm / 2.54,
    )

    label_width_px = int(DEFAULT_DPI * label_width_inch)
    label_height_px = int(DEFAULT_DPI * label_height_inch)

    max_label_rows = int(A4_PIXEL_HEIGHT_DEFAULT_DPI / label_height_px)
    max_label_cols = int(A4_PIXEL_WIDTH_DEFAULT_DPI / label_width_px)

    # Create grid of labels, create additional files if they don't fit in a single A4
    i = 0
    j = 0
    file_id = 0
    for index in range(len(product_names)):
        if i == max_label_rows:
            j += 1
            i = 0
        if j == max_label_cols:
            j = 0
            i = 0
            editor.save_current_img(
                target_file_name=editor.current_img_name, dpi=(DEFAULT_DPI, DEFAULT_DPI)
            )
        if i == 0 and j == 0:
            editor = ImageEditor(target_directory)
            file_id += 1
            editor.create_and_set_blank_image_as_current(
                size=(A4_PIXEL_WIDTH_DEFAULT_DPI, A4_PIXEL_HEIGHT_DEFAULT_DPI),
                format="bmp",
                target_filename=f"{target_file_name}_{file_id}",
            )

        # Draw label rectangle
        editor.insert_rectangle_to_current_img(
            rectangle_fill_color="white",
            x_coord=j * label_width_px,
            y_coord=i * label_height_px,
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
        editor.insert_text_to_current_img(
            text=f"{product_name}\n\nModel: {product_model}\nSN:{product_serial_number}",
            color="black",
            position=(
                j * label_width_px + offset_from_label_corners,
                i * label_height_px + offset_from_label_corners,
            ),
            max_width_pix=max_text_width_pix,
        )

        # Create QR code to serve as unique product identifier
        qreditor = ImageEditor(_tmp_dir_pathlib)
        qreditor.create_and_set_qr_code_image_as_current(
            code_content=f"{product_serial_number}"
        )

        desired_qr_code_width_pix = (label_width_px - max_text_width_pix) * 0.8

        qr_code_w, h = qreditor.get_current_img_size()

        barcode_resizing_factor = desired_qr_code_width_pix / qr_code_w

        qreditor.save_current_img()

        editor.insert_img_to_current_img(
            path_to_img=qreditor.current_img_path,
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

    editor.save_current_img(target_file_name=editor.current_img_name)
    qreditor.cleanup_tmp_dir()


if __name__ == "__main__":
    dataprocessor = DataProcessor(_results_dir_pathlib)
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
