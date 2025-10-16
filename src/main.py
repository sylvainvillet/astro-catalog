# Ensure Pillow is installed
try:
    from PIL import Image
except ImportError:
    import subprocess
    import sys
    print("Pillow not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

import flet as ft
from parameters import Parameters
from mosaic import build_mosaic, get_mosaic_dimensions
from catalog import Catalog
from special_objects import SpecialObject
from special_objects_editor import special_objects_editor
from utils import pil_to_base64
from enum import Enum
import copy

__version__ = "2.0.0"

messier_layout: list[SpecialObject] = [
    SpecialObject(numbers=[8, 20],       x=2, y=2, width=2, height=3),   # Lagoon Nebula
    SpecialObject(numbers=[16],          x=14, y=2, width=2, height=2),  # Eagle Nebula
    SpecialObject(numbers=[31, 32, 110], x=7, y=2, width=4, height=2),   # Andromeda
    SpecialObject(numbers=[33],          x=1, y=6, width=3, height=2),   # Triangulum Galaxy
    SpecialObject(numbers=[42, 43],      x=6, y=5, width=2, height=3),   # Orion Nebula
    SpecialObject(numbers=[45],          x=13, y=5, width=2, height=2),  # Pleiades
]

caldwell_layout: list[SpecialObject] = [
    SpecialObject(numbers=[20], x=1, y=1, width=3, height=2),   # North America Nebula
    SpecialObject(numbers=[33], x=11, y=2, width=2, height=3),  # Veil Nebula
    SpecialObject(numbers=[34], x=13, y=2, width=2, height=3),  # Veil Nebula
    SpecialObject(numbers=[68], x=7, y=2, width=2, height=2),   # Helix Nebula
    SpecialObject(numbers=[70], x=2, y=4, width=3, height=2),   # NGC 300
    SpecialObject(numbers=[71], x=7, y=7, width=4, height=2),   # Large Magellanic Cloud
    SpecialObject(numbers=[72], x=0, y=7, width=3, height=2),   # Small Magellanic Cloud
    SpecialObject(numbers=[99], x=14, y=6, width=3, height=2),  # Coalsack Nebula
]

MESSIER_PARAMETERS_KEY = "astro_catalog_parameters.messier"
CALDWELL_PARAMETERS_KEY = "astro_catalog_parameters.caldwell"
CATALOG_SELECTED_KEY = "astro_catalog_selected"

class Layout(Enum):
    BASIC = "Basic"
    ENHANCED = "Enhanced"

def main(page: ft.Page):
    print(f"Astro Catalog v{__version__}, created by Sylvain Villet")
    
    # Uncomment to clear storage during development
    # page.client_storage.clear()  

    # Load parameters from client storage or use defaults   
    if page.client_storage.contains_key(MESSIER_PARAMETERS_KEY):  # True if the key exists
        data = page.client_storage.get(MESSIER_PARAMETERS_KEY)
        messier_params = Parameters.from_dict(data if data is not None else {})
    else:
        messier_params = Parameters(
            output_file="messier_catalog.png",
            title=Catalog.MESSIER.title(),
            layout=copy.deepcopy(messier_layout),
        )

    if page.client_storage.contains_key(CALDWELL_PARAMETERS_KEY):  # True if the key exists
        data = page.client_storage.get(CALDWELL_PARAMETERS_KEY)
        caldwell_params = Parameters.from_dict(data if data is not None else {})
    else:
        caldwell_params = Parameters(
            output_file="caldwell_catalog.png",
            title=Catalog.CALDWELL.title(),
            catalog=Catalog.CALDWELL,
            layout=copy.deepcopy(caldwell_layout)
        )

    catalog_prefix = Catalog.MESSIER.prefix()
    if page.client_storage.contains_key(CATALOG_SELECTED_KEY):  # True if the key exists
        catalog_prefix = page.client_storage.get(CATALOG_SELECTED_KEY)
    
    params = messier_params if catalog_prefix == Catalog.MESSIER.prefix() else caldwell_params
    layout_type: str = Layout.BASIC.value if params.layout.count == 0 else Layout.ENHANCED.value
    pil_image: Image.Image

    def get_catalogs_options() -> list[ft.DropdownOption]:
        options: list[ft.DropdownOption] = []
        for catalog in Catalog:
            options.append(
                ft.DropdownOption(
                    key=catalog.prefix(),
                    text=catalog.title()
                )
            )
        return options
    
    def catalog_changed(e: ft.ControlEvent):
        nonlocal params, catalog_prefix, messier_params, caldwell_params
        
        # Save params values in the current params object
        if params.catalog == Catalog.MESSIER:
            messier_params = params
        elif params.catalog == Catalog.CALDWELL:
            caldwell_params = params
        catalog_prefix = e.control.value
        params = messier_params if catalog_prefix == Catalog.MESSIER.prefix() else caldwell_params
        input_folder_field.value = params.input_folder
        title_field.value = params.title
        scale_slider.value = params.scale
        refresh_resolution_label()
        generate(None)
        page.update()

    def get_layout_options() -> list[ft.DropdownOption]:
        options: list[ft.DropdownOption] = []
        for layout in Layout:
            options.append(
                ft.DropdownOption(
                    key=layout.value,
                    text=layout.value
                )
            )
        return options
    
    def layout_changed(e: ft.ControlEvent):
        nonlocal params, layout_type
        layout_type = e.control.value
        print(f"Layout changed to {layout_type}")
        if layout_type == Layout.BASIC.value:
            params.layout = []
        elif layout_type == Layout.ENHANCED.value:
            if params.catalog == Catalog.MESSIER:
                params.layout = copy.deepcopy(messier_layout)
            elif params.catalog == Catalog.CALDWELL:
                params.layout = copy.deepcopy(caldwell_layout)
        page.update()
        generate(None)


    def open_editor_dialog(e):
        objects_copy, table = special_objects_editor(page, params.layout)

        def apply_changes(_):
            # Copy all values from fields to original list
            new_list = []
            for obj in objects_copy:
                try:
                    numbers = [int(x.strip()) for x in obj._fields[0].value.split(",") if x.strip()]
                    x = int(obj._fields[1].value)
                    y = int(obj._fields[2].value)
                    width = int(obj._fields[3].value)
                    height = int(obj._fields[4].value)
                    new_list.append(SpecialObject(numbers=numbers, x=x, y=y, width=width, height=height))
                except ValueError:
                    page.update()
                    return
            # Apply to original
            params.layout.clear()
            params.layout.extend(new_list)
            page.close(dialog)
            generate(None)

        def cancel_changes(e):
            page.close(dialog)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Layout"),
            content=ft.Container(width=700, height=400, content=table),
            actions=[
                ft.TextButton("Cancel", on_click=cancel_changes),
                ft.ElevatedButton("Apply", on_click=apply_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)

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
        page.update()

    def column_changed_ended(e: ft.ControlEvent):
        generate(None)

    def confirm_reset_dialog(e):
        def on_confirm(e):
            page.close(confirm_dialog)
            reset_layout(e)

        def on_cancel(e):
            page.close(confirm_dialog)

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Reset"),
            content=ft.Text("Are you sure you want to reset the layout? This will discard any custom changes."),
            actions=[
                ft.TextButton("Cancel", on_click=on_cancel),
                ft.ElevatedButton("Confirm", on_click=on_confirm),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(confirm_dialog)

    def reset_layout(e: ft.ControlEvent):
        nonlocal params, layout_type, layout_dropdown, columns_slider

        if params.catalog == Catalog.MESSIER:
            params.layout = copy.deepcopy(messier_layout)
        elif params.catalog == Catalog.CALDWELL:
            params.layout = copy.deepcopy(caldwell_layout)

        layout_type = Layout.ENHANCED.value
        layout_dropdown.value = layout_type
        
        params.grid_cols = 17
        columns_slider.value = params.grid_cols

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

    def generate(_):
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
        if params.catalog == Catalog.MESSIER:
            page.client_storage.set(MESSIER_PARAMETERS_KEY, params.to_dict())
        elif params.catalog == Catalog.CALDWELL:
            page.client_storage.set(CALDWELL_PARAMETERS_KEY, params.to_dict())
        page.client_storage.set(CATALOG_SELECTED_KEY, params.catalog.prefix())

        buttons_row.disabled = False
        page.update()

    def save_image(_):
        if pil_image:
            # Extract folder and file name from output_file
            file_name = params.output_file.split("/")[-1]
            initial_directory = "/".join(params.output_file.split("/")[:-1])
            output_file_picker.save_file(file_name=file_name, 
                                         initial_directory=initial_directory, 
                                         allowed_extensions=[".png", ".jpg", ".jpeg", ".tiff"])

    def output_file_result(e: ft.FilePickerResultEvent):
        # Check if path is empty
        if not e.path:
            return
        params.output_file = e.path or ""
        if pil_image:
            pil_image.save(params.output_file)
            success_dialog = ft.AlertDialog(title=ft.Text("Success"), 
                                            content=ft.Text(f"Image saved successfully."), 
                                            actions=[ft.TextButton("OK", on_click=lambda e: page.close(success_dialog))])
            page.open(success_dialog)

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
                            label="Mode",
                            options=get_layout_options(),
                            value=layout_type,
                            on_change=layout_changed)

    columns_slider = ft.Slider(
        value=params.grid_cols,
        min=5,
        max=25,
        divisions=19,
        on_change=column_changed,
        on_change_end=column_changed_ended,
        label="{value}",
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
    buttons_row = ft.Row([save_button], alignment=ft.MainAxisAlignment.CENTER)

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
                        value=catalog_prefix,
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
                    ft.Text("Layout:"),
                    ft.Row([
                        layout_dropdown,
                        ft.ElevatedButton(
                            "Edit",
                            icon=ft.Icons.EDIT,
                            on_click=open_editor_dialog,
                        ),
                    ]),
                    ft.Row([
                        ft.Text("Columns:"),
                        columns_slider,
                    ]),
                    ft.ElevatedButton(
                        "Reset Layout",
                        icon=ft.Icons.UNDO,
                        on_click=confirm_reset_dialog,
                    ),
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
