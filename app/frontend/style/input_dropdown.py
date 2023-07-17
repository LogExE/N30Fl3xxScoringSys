import flet as ft
from style.custom_input import ONE_FIELD_WIDTH


class InputDropdown(ft.UserControl):
    def __init__(self, options, width):
        self.input: ft.Control = ft.Dropdown(
            height=40,
            width=width * ONE_FIELD_WIDTH,
            text_size=14,
            text_style=ft.TextStyle.weight,
            content_padding=5,
            offset=(0, -0.3),
            options=[ft.dropdown.Option(option) for option in options],

            # bgcolor=ft.colors.RED_100
        )
        super().__init__()

    #     self.status: ft.Control = ft.Container(
    #         offset=(0, -0.3),
    #         bgcolor=ft.colors.RED_100,
    #         visible=False
    #     )
    #
    # def set_error(self, e):
    #     if e:
    #         self.status.visible = True
    #     else:
    #         self.status.visible = False


    # def build(self):
    #     return ft.Stack(
    #         controls=[
    #             self.status,
    #             self.input
    #         ]
    #     )

    def build(self):
        return self.input
