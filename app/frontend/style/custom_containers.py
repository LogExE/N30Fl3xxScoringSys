import flet as ft


ONE_FIELD_WIDTH = 170

def CustomColumn(controls):
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        controls=controls
    )


def CustomContainer(controls):
    return ft.Container(
        bgcolor=ft.colors.with_opacity(0.2, ft.colors.OUTLINE_VARIANT),
        padding=25,
        border_radius=30,
        content=CustomColumn(controls)
    )

#
# def CustomDropdown(options, width):
#     return ft.Dropdown(
#         height=40,
#         width=width*ONE_FIELD_WIDTH,
#         text_size=14,
#         text_style=ft.TextStyle.weight,
#         content_padding=5,
#         offset=(0, -0.3),
#         options=[ft.dropdown.Option(option) for option in options],
#     )
