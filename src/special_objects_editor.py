import copy
import flet as ft
from special_objects import SpecialObject

def special_objects_editor(page: ft.Page, original_objects: list[SpecialObject]) -> tuple[list[SpecialObject], ft.Column]:
    """
    Returns a container with an editable table.
    Changes are applied to a copy and only saved to original_objects on Apply.
    """
    # Work on a deep copy so Cancel discards changes
    objects = copy.deepcopy(original_objects)

    table = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    def refresh_table():
        table.controls.clear()

        for idx, obj in enumerate(objects):
            numbers_field = ft.TextField(
                value=",".join(map(str, obj.numbers)), width=140, label="Number(s)", dense=True
            )
            x_field = ft.TextField(value=str(obj.x), width=100, label="Column", dense=True)
            y_field = ft.TextField(value=str(obj.y), width=100, label="Row", dense=True)
            w_field = ft.TextField(value=str(obj.width), width=100, label="Width", dense=True)
            h_field = ft.TextField(value=str(obj.height), width=100, label="Height", dense=True)

            # Store references in the object for later Apply
            obj._fields = (numbers_field, x_field, y_field, w_field, h_field)

            def delete_clicked(e, i=idx):
                objects.pop(i)
                refresh_table()
                page.update()

            row = ft.Row(
                [
                    numbers_field,
                    x_field,
                    y_field,
                    w_field,
                    h_field,
                    ft.IconButton(ft.Icons.DELETE, tooltip="Delete", on_click=delete_clicked),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            )
            table.controls.append(row)

        # Add new object row
        add_numbers = ft.TextField(label="Number(s)", width=140, dense=True, on_submit=lambda e: add_clicked(e))
        add_x = ft.TextField(label="Column", width=100, dense=True, on_submit=lambda e: add_clicked(e))
        add_y = ft.TextField(label="Row", width=100, dense=True, on_submit=lambda e: add_clicked(e))
        add_w = ft.TextField(label="Width", width=100, dense=True, on_submit=lambda e: add_clicked(e))
        add_h = ft.TextField(label="Height", width=100, dense=True, on_submit=lambda e: add_clicked(e))

        def add_clicked(e):
            try:
                new_obj = SpecialObject(
                    numbers=[int(x.strip()) for x in add_numbers.value.split(",") if x.strip()],
                    x=int(add_x.value),
                    y=int(add_y.value),
                    width=int(add_w.value),
                    height=int(add_h.value),
                )
                new_obj._fields = (add_numbers, add_x, add_y, add_w, add_h)
                objects.append(new_obj)
                refresh_table()
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Invalid numeric value"))
                page.snack_bar.open = True
                page.update()

        table.controls.append(
            ft.Row(
                [add_numbers, add_x, add_y, add_w, add_h, ft.IconButton(ft.Icons.ADD, tooltip="Add", on_click=add_clicked)],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            )
        )

    refresh_table()
    return objects, table
