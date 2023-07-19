import flet as ft
from style.custom_containers import ONE_FIELD_WIDTH


class InputRadio(ft.Container):
    def __init__(self, options):
        super().__init__()
        self.content = ft.RadioGroup(ft.Row(
            [ft.Radio(value=key, label=options[key]) for key in options.keys()]
        ))
        self.width = 1.70 * ONE_FIELD_WIDTH
        self.offset = (0, -0.3)

        self.border = None
        self.border_radius = 5

    def set_error(self, e):
        if e:
            self.border = ft.border.all(width=2, color=ft.colors.RED_500)
        else:
            self.border = None

        self.update()
