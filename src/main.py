import flet as ft
from parameters import Parameters
from mosaic import build_mosaic, get_mosaic_dimensions
from catalog import Catalog
from special_objects import SpecialObject

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
    SpecialObject(numbers=[33], x=14, y=1, width=2, height=3),  # Veil Nebula
    SpecialObject(numbers=[68], x=7, y=2, width=2, height=2),   # Helix Nebula
    SpecialObject(numbers=[70], x=2, y=4, width=3, height=2),   # NGC 300
    SpecialObject(numbers=[71], x=9, y=5, width=4, height=2),   # Large Magellanic Cloud
    SpecialObject(numbers=[72], x=0, y=7, width=3, height=2),   # Small Magellanic Cloud
    SpecialObject(numbers=[99], x=14, y=6, width=3, height=2),  # Coalsack Nebula
]

def main(page: ft.Page):
    params = Parameters(
        layout=messier_layout,
    )
    catalog_prefix: str = Catalog.MESSIER.prefix()

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
        catalog_prefix = e.control.value
        params.catalog = next(cat for cat in Catalog if cat.prefix() == catalog_prefix)
        if params.catalog == Catalog.MESSIER:
            params.layout = messier_layout
        elif params.catalog == Catalog.CALDWELL:
            params.layout = caldwell_layout
        page.update()

    def input_folder_result(e: ft.FilePickerResultEvent):
        input_folder_field.value = e.path
        params.input_folder = e.path or ""
        input_folder_field.update()

    def output_file_result(e: ft.FilePickerResultEvent):
        output_file_field.value = e.path
        params.output_file = e.path or ""
        output_file_field.update()

    def scale_changed(e: ft.ControlEvent):
        params.scale = e.control.value
        refresh_resolution_label()
        page.update()

    def refresh_resolution_label():
        width, height = get_mosaic_dimensions(params)
        thumb_size = params.get_thumb_size_scaled()
        output_resolution_label.value = f"Output resolution: %d x %d px (%d x %d px per square)" % (width, height, thumb_size, thumb_size)
        page.update()

    def generate(_):
        build_mosaic(params)

    page.title = "Astro Catalog"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_folder_picker = ft.FilePicker(on_result=input_folder_result)
    page.overlay.append(input_folder_picker)
    page.update()
    input_folder_field = ft.TextField(label="Input folder", 
                                      value=params.input_folder,
                                      expand=True,
                                      width=300)
    
    output_file_picker = ft.FilePicker(on_result=output_file_result)
    page.overlay.append(output_file_picker)
    page.update()
    output_file_field = ft.TextField(label="Output file", 
                                     value=params.output_file,
                                     expand=True,
                                     width=300)

    output_resolution_label = ft.Text()
    refresh_resolution_label() 

    page.add(
        ft.Column([
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
            ft.Row([
                output_file_field,
                ft.ElevatedButton(
                    "Browse",
                    icon=ft.Icons.IMAGE,
                    on_click=lambda _: output_file_picker.save_file(),
                )
            ]),
            ft.Text("Scale:"),
            ft.Slider(
                value=params.scale,
                min=1,
                max=10,
                divisions=9,
                on_change=scale_changed
            ),
            output_resolution_label,
            ft.ElevatedButton(
                "Generate",
                icon=ft.Icons.ROCKET,
                on_click=generate,
            )
        ])
    )

ft.app(main)
