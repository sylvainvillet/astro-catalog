# Ensure Pillow is installed
try:
    from PIL import Image
except ImportError:
    import subprocess
    import sys
    print("Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

import os
import flet as ft
from parameters import LayoutMode, Parameters
from mosaic import build_mosaic, get_mosaic_dimensions
from catalog import Catalog
from storage import Storage
from special_objects_editor import open_special_objects_editor
from utils import pil_to_base64
import copy

__version__ = "2.1.0"

def main(page: ft.Page):
    print(f"Astro Catalog v{__version__}, created by Sylvain Villet")
    
    # Load parameters from client storage or use defaults   
    storage = Storage(page)

    # Uncomment to clear storage during development
    # storage.clear() 
    
    params: Parameters = storage.load_parameters()
    pil_image: Image.Image

    def get_catalogs_options() -> list[ft.dropdown.Option]:
        options: list[ft.dropdown.Option] = []
        for catalog in Catalog:
            options.append(
                ft.dropdown.Option(
                    key=catalog.id(),
                    text=catalog.title()
                )
            )
        return options
    
    def catalog_changed(e: ft.ControlEvent):
        nonlocal params
        
        # Save params values in the current params object
        storage.save_parameters(params)
        catalog = Catalog.from_id(e.control.value)
        storage.save_catalog(catalog)
        params = storage.load_parameters()
        input_folder_field.value = params.input_folder
        title_field.value = params.title
        progress_switch.value = params.show_progress
        scale_slider.value = params.scale
        refresh_layout_controls()
        refresh_resolution_label()
        generate(None)
        page.update()

    def get_layout_options() -> list[ft.dropdown.Option]:
        options: list[ft.dropdown.Option] = []
        for layout in LayoutMode:
            options.append(
                ft.dropdown.Option(
                    key=layout.value,
                    text=layout.value
                )
            )
        return options
    
    def layout_changed(e: ft.ControlEvent):
        nonlocal params
        params.layout_mode = LayoutMode(e.control.value)
        refresh_layout_controls()
        page.update()
        generate(None)

    def input_folder_result(e: ft.FilePickerResultEvent):
        # Check if path is empty
        if not e.path:
            return
        input_folder_field.value = e.path
        params.input_folder = e.path or ""
        input_folder_field.update()
        generate(None)

    def column_changed(e: ft.ControlEvent):
        params.grid_cols = int(round(e.control.value))
        refresh_resolution_label()
        page.update()

    def column_changed_ended(e: ft.ControlEvent):
        generate(None)

    def confirm_reset_dialog(e: ft.ControlEvent):
        def on_confirm(_: ft.ControlEvent):
            page.close(confirm_dialog)
            reset_layout()

        def on_cancel(_: ft.ControlEvent):
            page.close(confirm_dialog)

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Restore Default Layout"),
            content=ft.Text("Are you sure you want to restore the default layout? This will discard any custom changes."),
            actions=[
                ft.TextButton("Cancel", on_click=on_cancel),
                ft.ElevatedButton("Confirm", on_click=on_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(confirm_dialog)

    def reset_layout():
        nonlocal params, layout_dropdown, columns_slider

        # Restore default layout for the current catalog
        default_params = Parameters.default(params.catalog)
        params.layout = copy.deepcopy(default_params.layout)
        params.layout_mode = default_params.layout_mode
        params.grid_cols = default_params.grid_cols
        refresh_layout_controls()

        page.update()
        generate(None)

    def refresh_layout_controls():
        nonlocal edit_layout_button, layout_dropdown
        layout_dropdown.value = params.layout_mode.value
        edit_layout_button.disabled = params.layout_mode == LayoutMode.BASIC
        columns_slider.value = params.grid_cols
        page.update()

    def progress_switch_changed(e: ft.ControlEvent):
        params.show_progress = e.control.value
        page.update()
        generate(None)

    def scale_changed(e: ft.ControlEvent):
        params.scale = e.control.value
        refresh_resolution_label()
        page.update()

    def scale_change_ended(e: ft.ControlEvent):
        generate(None)

    def refresh_resolution_label():
        width, height = get_mosaic_dimensions(params)
        thumb_size = params.get_thumb_size_scaled()
        output_resolution_label.value = f"Output resolution: %d x %d px (%d x %d px per square)" % (width, height, thumb_size, thumb_size)
        page.update()

    def generate(_: ft.ControlEvent | None):
        nonlocal pil_image
        
        buttons_row.disabled = True
        container.controls[0] = placeholder  # loading indicator
        page.update()

        pil_image = build_mosaic(params)
        output_image = ft.Image(src_base64=pil_to_base64(pil_image), 
                                fit=ft.ImageFit.CONTAIN, 
                                expand=True)
        container.controls[0] = output_image  # put back image
        
        # Save parameters to client storage
        storage.save_parameters(params)
        storage.save_catalog(params.catalog)
        buttons_row.disabled = False
        page.update()

    def save_image(_: ft.ControlEvent | None):
        if pil_image:
            file_name = os.path.basename(params.output_file)
            initial_directory = os.path.dirname(params.output_file)

            # Ensure it exists and use OS-specific separators
            initial_directory = os.path.normpath(initial_directory)

            if not os.path.isdir(initial_directory):
                # fallback to home directory
                initial_directory = os.path.expanduser("~")

            print(f"Open Save As dialog to {initial_directory} with file name {file_name}")

            # Extract folder and file name from output_file
            output_file_picker.save_file(file_name=file_name, 
                                         initial_directory=initial_directory, 
                                         allowed_extensions=[".png", ".jpg", ".jpeg", ".tiff"])

    def output_file_result(e: ft.FilePickerResultEvent):
        # Check if path is empty
        if not e.path:
            return
        params.output_file = e.path or ""
        storage.save_parameters(params)
        if pil_image:
            try:
                pil_image.save(params.output_file)
                success_dialog = ft.AlertDialog(title=ft.Text("Success"), 
                                                content=ft.Text(f"Image saved successfully."), 
                                                actions=[ft.TextButton("OK", on_click=lambda e: page.close(success_dialog))])
                page.open(success_dialog)
            except Exception as ex:
                print(f"Error saving image: {ex}")
                error_dialog = ft.AlertDialog(title=ft.Text("Error"), 
                                               content=ft.Text(f"Failed to save image: {ex}"), 
                                               actions=[ft.TextButton("OK", on_click=lambda e: page.close(error_dialog))])
                page.open(error_dialog)

    page.title = "Astro Catalog"
    page.window.maximized = True
    #page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_folder_picker = ft.FilePicker(on_result=input_folder_result)
    page.overlay.append(input_folder_picker)
    input_folder_field = ft.TextField(label="Images folder", 
                                      value=params.input_folder,
                                      expand=True,
                                      width=300,
                                      on_change=lambda e: setattr(params, "input_folder", e.control.value))
    
    output_file_picker = ft.FilePicker(on_result=output_file_result)
    page.overlay.append(output_file_picker)

    title_field = ft.TextField(label="Title", 
                                value=params.title,
                                expand=True,
                                width=300,
                                on_change=lambda e: setattr(params, "title", e.control.value),
                                on_submit=generate)

    layout_dropdown = ft.Dropdown(
                            editable=True,
                            label="Layout",
                            options=get_layout_options(),
                            value=params.layout_mode.value,
                            on_change=layout_changed)
    edit_layout_button = ft.ElevatedButton(
                            "Edit",
                            icon=ft.Icons.EDIT,
                            on_click=lambda _: open_special_objects_editor(page, params.layout, lambda: generate(None)))
    edit_layout_button.disabled = params.layout_mode == LayoutMode.BASIC

    columns_slider = ft.Slider(
        value=params.grid_cols,
        min=5,
        max=25,
        divisions=19,
        on_change=column_changed,
        on_change_end=column_changed_ended,
        label="{value}",
    )

    progress_switch = ft.Switch(
        value=params.show_progress,
        on_change=progress_switch_changed,
    )

    scale_slider = ft.Slider(
        value=params.scale,
        min=1,
        max=10,
        divisions=9,
        on_change=scale_changed,
        on_change_end=scale_change_ended,
    )

    output_resolution_label = ft.Text()
    refresh_resolution_label() 

    save_button = ft.ElevatedButton(
        "Save",
        icon=ft.Icons.SAVE,
        on_click=save_image,
    )
    reset_button = ft.ElevatedButton(
                        "Restore Default Layout",
                        icon=ft.Icons.UNDO,
                        on_click=confirm_reset_dialog
    )
    buttons_row = ft.Row([save_button, reset_button], alignment=ft.MainAxisAlignment.CENTER)

    placeholder = ft.ProgressRing(width=50, height=50)
    container = ft.Column([placeholder], expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    left_panel = ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text("Astro Catalog", style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD)),
                            ft.Text("Select a catalog and specify the input folder containing your images", style=ft.TextStyle(size=14)),
                            ft.Text(f"Created by Sylvain Villet (v{__version__})", style=ft.TextStyle(size=12)),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Dropdown(
                        editable=True,
                        label="Catalog",
                        options=get_catalogs_options(),
                        value=params.catalog.id(),
                        on_change=catalog_changed,
                    ),
                    ft.Row([
                        input_folder_field,
                        ft.ElevatedButton(
                            "Browse",
                            icon=ft.Icons.FOLDER,
                            on_click=lambda _: input_folder_picker.get_directory_path(),
                        )
                    ]),
                    title_field,
                    ft.Row([
                        layout_dropdown,
                        edit_layout_button,
                    ]),
                    ft.Row([
                        ft.Text("Columns:"),
                        columns_slider,
                    ]),
                    ft.Row([
                        ft.Text("Show Progress:"),
                        progress_switch,
                    ]),
                    ft.Row([
                        ft.Text("Scale:"),
                        scale_slider,
                    ]),
                    output_resolution_label,
                    buttons_row
                ], 
                scroll=ft.ScrollMode.AUTO,
                spacing=20)

    page.add(
            ft.Row([
                left_panel,
                container
            ], 
            vertical_alignment=ft.CrossAxisAlignment.START, 
            alignment=ft.MainAxisAlignment.CENTER, 
            expand=True)
    )

    generate(None)  # Initial generation

ft.app(main)
