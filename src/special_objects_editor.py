import copy
import flet as ft
from special_objects import SpecialObject

FIELD_WIDTH = 100

def open_special_objects_editor(page: ft.Page, data: list[SpecialObject], on_apply: callable):
    # Make a deep copy of data so Cancel doesn't affect original
    import copy
    data_copy = copy.deepcopy(data)

    rows: list[ft.Row] = []
    fields_refs: list[dict[str, ft.TextField]] = []

    # Helper to create a row
    def make_row(obj: SpecialObject | None = None) -> ft.Row:
        numbers = ft.TextField(
            value=",".join(str(n) for n in obj.numbers) if obj else "",
            label="Numbers",
            width=150,
        )
        x = ft.TextField(value=str(obj.x) if obj else "", label="Column", width=FIELD_WIDTH)
        y = ft.TextField(value=str(obj.y) if obj else "", label="Row", width=FIELD_WIDTH)
        width = ft.TextField(value=str(obj.width) if obj else "", label="Width", width=FIELD_WIDTH)
        height = ft.TextField(value=str(obj.height) if obj else "", label="Height", width=FIELD_WIDTH)

        ref = {"numbers": numbers, "x": x, "y": y, "width": width, "height": height}
        fields_refs.append(ref)

        remove_btn = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Remove this object",
            on_click=lambda e: remove_row(row_container, ref),
        )

        row_container = ft.Row(
            [numbers, x, y, width, height, remove_btn],
            alignment=ft.MainAxisAlignment.START,
        )

        return row_container

    # Remove row
    def remove_row(row: ft.Row, ref: dict[str, ft.TextField]):
        if row in rows:
            rows.remove(row)
        if ref in fields_refs:
            fields_refs.remove(ref)
        editor_col.controls.remove(row)
        page.update()

    # Add new row
    def add_new_row(_):
        new_row = make_row()
        rows.append(new_row)
        editor_col.controls.insert(len(editor_col.controls) - 1, new_row)
        page.update()

    # Apply all changes
    def apply_changes(_):
        nonlocal data
        new_data: list[SpecialObject] = []

        for ref in fields_refs:
            # Skip completely empty rows
            if not any(ref[f].value.strip() for f in ref):
                continue
            try:
                new_obj = SpecialObject(
                    numbers=[int(x.strip()) for x in ref["numbers"].value.split(",") if x.strip()],
                    x=int(ref["x"].value),
                    y=int(ref["y"].value),
                    width=int(ref["width"].value),
                    height=int(ref["height"].value),
                )
                new_data.append(new_obj)
            except ValueError:
                # Ignore invalid rows silently (could show an alert instead)
                pass

        # Replace the original list contents
        data.clear()
        data.extend(new_data)

        page.close(dialog)
        
        # Call the callback if provided
        if on_apply:
            on_apply()

    # Cancel edits
    def cancel_changes(e):
        page.close(dialog)

    # Build UI
    editor_col = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Add existing rows
    # Sort objects by the first number in their 'numbers' list; objects with empty 'numbers' are sorted last due to float('inf')
    for obj in sorted(data_copy, key=lambda o: o.numbers[0] if o.numbers else float('inf')):
        row = make_row(obj)
        rows.append(row)
        editor_col.controls.append(row)

    # Add button bar
    button_row = ft.Row(
        [
            ft.ElevatedButton("Add Row", on_click=add_new_row),
            ft.Row(
                [
                    ft.TextButton("Cancel", on_click=cancel_changes),
                    ft.FilledButton("Apply", on_click=apply_changes),
                ]
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    editor_col.controls.append(button_row)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Edit Special Objects"),
        content=ft.Container(content=editor_col, width=700),
    )

    page.open(dialog)
    page.update()