import flet as ft
from style.custom_containers import ONE_FIELD_WIDTH


class InputDropdown(ft.Dropdown):
    def __init__(self, options, width):
        super().__init__()
        self.height = 40
        self.width = width * ONE_FIELD_WIDTH
        self.text_size = 14
        self.text_style = ft.TextStyle.weight
        self.content_padding = 5
        self.offset = (0, -0.3)

        self.options = [ft.dropdown.Option(option) for option in options]

        self.border_color = ft.colors.BLACK
        self.border_width = 1
        self.focused_border_color = ft.colors.DEEP_PURPLE_500
        self.focused_border_width = 2
        self.hint_text = " "

    def set_error(self, e):
        if e:
            self.border_color = ft.colors.RED_500
            self.focused_border_color = ft.colors.RED_500
            self.border_width = 2
            self.hint_text = "Выберите значение"
        else:
            self.border_color = ft.colors.BLACK
            self.focused_border_color = ft.colors.DEEP_PURPLE_500
            self.border_width = 1
            self.hint_text = " "

        self.update()
