
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
                value=",".join(map(str, obj.numbers)), width=140, label="Numbers", dense=True
            )
            x_field = ft.TextField(value=str(obj.x), width=60, label="x", dense=True)
            y_field = ft.TextField(value=str(obj.y), width=60, label="y", dense=True)
            w_field = ft.TextField(value=str(obj.width), width=80, label="width", dense=True)
            h_field = ft.TextField(value=str(obj.height), width=80, label="height", dense=True)

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
        add_numbers = ft.TextField(label="Numbers", width=140, dense=True)
        add_x = ft.TextField(label="x", width=60, dense=True)
        add_y = ft.TextField(label="y", width=60, dense=True)
        add_w = ft.TextField(label="width", width=80, dense=True)
        add_h = ft.TextField(label="height", width=80, dense=True)

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


def build_editor_ui_old(page: ft.Page, special_objects: list[SpecialObject]):
    """Return a Container with the editable table of SpecialObjects."""

    table = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    def refresh_table():
        table.controls.clear()

        for idx, obj in enumerate(special_objects):
            numbers_field = ft.TextField(
                value=",".join(map(str, obj.numbers)), width=140, label="Numbers", dense=True
            )
            x_field = ft.TextField(value=str(obj.x), width=60, label="x", dense=True)
            y_field = ft.TextField(value=str(obj.y), width=60, label="y", dense=True)
            w_field = ft.TextField(value=str(obj.width), width=80, label="width", dense=True)
            h_field = ft.TextField(value=str(obj.height), width=80, label="height", dense=True)

            def update_clicked(e, i=idx, nf=numbers_field, xf=x_field, yf=y_field, wf=w_field, hf=h_field):
                try:
                    print(f"Updating {special_objects[i]}")
                    special_objects[i].numbers = [int(x.strip()) for x in nf.value.split(",") if x.strip()]
                    special_objects[i].x = int(xf.value)
                    special_objects[i].y = int(yf.value)
                    special_objects[i].width = int(wf.value)
                    special_objects[i].height = int(hf.value)
                    print(f"With {special_objects[i]}")
                    page.update()
                except ValueError:
                    page.update()

            def delete_clicked(e, i=idx):
                special_objects.pop(i)
                refresh_table()
                page.update()

            row = ft.Row(
                [
                    numbers_field,
                    x_field,
                    y_field,
                    w_field,
                    h_field,
                    ft.IconButton(ft.Icons.SAVE, tooltip="Update", on_click=update_clicked),
                    ft.IconButton(ft.Icons.DELETE, tooltip="Delete", on_click=delete_clicked),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            )
            table.controls.append(row)

        # --- Add new object row ---
        add_numbers = ft.TextField(label="Numbers", width=140, dense=True)
        add_x = ft.TextField(label="x", width=60, dense=True)
        add_y = ft.TextField(label="y", width=60, dense=True)
        add_w = ft.TextField(label="width", width=80, dense=True)
        add_h = ft.TextField(label="height", width=80, dense=True)

        def add_clicked(e):
            try:
                new_obj = SpecialObject(
                    numbers=[int(x.strip()) for x in add_numbers.value.split(",") if x.strip()],
                    x=int(add_x.value),
                    y=int(add_y.value),
                    width=int(add_w.value),
                    height=int(add_h.value),
                )
                print(f"Adding {new_obj}")
                special_objects.append(new_obj)
                refresh_table()
                page.update()
            except ValueError:
                refresh_table()
                page.update()

        table.controls.append(
            ft.Row(
                [add_numbers, add_x, add_y, add_w, add_h, ft.IconButton(ft.Icons.ADD, tooltip="Add", on_click=add_clicked)],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            )
        )

    refresh_table()
    return ft.Container(
        width=700,
        height=400,
        content=ft.Column(
            [table],
            scroll=ft.ScrollMode.AUTO,
        ),
    )
