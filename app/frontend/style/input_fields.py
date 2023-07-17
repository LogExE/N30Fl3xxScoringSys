import flet as ft
from style.custom_input import ONE_FIELD_WIDTH


class InputFields(ft.UserControl):
    def __init__(self, title, width, max_length=None, hint_text=None, suffix_text=None):
        self.input: ft.Control = ft.TextField(
            label=title,
            height=60,
            width=width*ONE_FIELD_WIDTH,
            capitalization="WORDS",

            max_length=max_length,
            counter_text=" ",
            expand=True,

            hint_text=hint_text,
            hint_style=ft.TextStyle(size=14, weight=ft.FontWeight.NORMAL),

            suffix_text=suffix_text
        )
        super().__init__()

    def build(self):
        return self.input
